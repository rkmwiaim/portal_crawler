import time

from functional import seq
import external.mysql_api as mysql_api
from crawler import crawler_factory
from definitions import log
from processor.crawling_context_sheet import CrawlingContextSheet, get_channel_key
from processor.crawling_data_sheet import CrawlingDataSheet
import config

crawler_dict = {
  '네이버뉴스': crawler_factory.naver_news_crawler,
  '네이버블로그': crawler_factory.naver_blog_crawler,
  '네이버카페': crawler_factory.naver_cafe_crawler
}


class CrawlProcessor:
  def __init__(self, portal, channel,
               crawling_context_sheet_class=CrawlingContextSheet,
               crawling_data_sheet_class=CrawlingDataSheet,
               data_base=mysql_api
               ):
    contexts = crawling_context_sheet_class().get()
    self.max_crawl_page = config.MAX_CRAWL_PAGE
    channel_key = get_channel_key(portal, channel)

    self.crawling_data_sheet_class = crawling_data_sheet_class
    self.data_base = data_base

    log.info(f'Processor channel key: {channel_key}, max crawl page: {self.max_crawl_page}')

    self.crawler = crawler_dict.get(channel_key)
    self.context = contexts.get(channel_key)

    self.check_init()

  def check_init(self):
    if self.crawler is None:
      raise ValueError(f'Crawler has yet defined.')

    if self.context is None:
      raise ValueError(f'context has yet defined.')

  def start(self):
    self.process_context(self.context)

  def process_context(self, context):
    context_start_time = time.time()

    channel_key = context['portal'] + context['channel']
    log.info('start to crawl channel [{}].'.format(context))

    crawler = crawler_dict[channel_key]
    data_sheet = self.crawling_data_sheet_class(context)
    start_url = context['start_url']
    new_articles = self.crawl(int(context['crawl_page']), crawler, start_url)
    new_articles = new_articles.distinct_by(lambda a: a['url']).sorted(key=lambda d: d['posted_at'])

    log.info(f'# total new articles: {new_articles.size()}')

    if new_articles.size() > 0:
      new_articles.for_each(self.data_base.insert)
      data_sheet.append(new_articles)

    log.info(
      f'crawled channel key [{channel_key}] finished. # new channel: {new_articles.size()}, crawling time: {time.time() - context_start_time}')

  def crawl(self, min_crawl_page, crawler, start_url):
    new_articles = seq([])
    checked_count = 0

    for i in range(0, self.max_crawl_page):
      start_index = i * 10 + 1
      url = start_url + '&start={}'.format(start_index)
      articles = crawler.crawl_url(url)
      urls = articles.map(lambda d: d['url']).to_set()
      checked_urls = self.data_base.check_urls(urls)
      checked_count += len(checked_urls)

      new_urls = urls - checked_urls
      log.info(f'# new urls: {len(new_urls)}')
      new_articles += articles.filter(lambda a: a['url'] in new_urls)

      if i >= (min_crawl_page - 1) and len(new_urls) == 0:
        break

    return new_articles


if __name__ == '__main__':
  processor = CrawlProcessor()
  processor.start()
