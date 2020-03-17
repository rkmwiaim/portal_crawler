import time

from functional import seq

from crawler import crawler_factory
from definitions import log
from processor.crawler_data_base import CrawlerDataBase
from processor.crawling_context_sheet import CrawlingContextSheet
from processor.crawling_data_sheet import CrawlingDataSheet
import config

crawler_dict = {
  '네이버뉴스': crawler_factory.naver_news_crawler
}


class CrawlProcessor:
  def __init__(self, max_crawl_page=config.MAX_CRAWL_PAGE):
    self.data_base = CrawlerDataBase()
    self.max_crawl_page = max_crawl_page

  def start(self):
    context_sheet = CrawlingContextSheet()
    contexts = context_sheet.get()
    for context in contexts:
      self.process_context(context)

  def process_context(self, context):
    context_start_time = time.time()

    channel_key = context['portal'] + context['channel']
    log.info('start to crawl channel [{}].'.format(context))

    crawler = crawler_dict[channel_key]
    data_sheet = CrawlingDataSheet(context)
    start_url = context['start_url']
    new_articles = self.crawl(int(context['crawl_page']), crawler, start_url)
    new_articles = new_articles.distinct_by(lambda a: a['url'])

    new_articles.for_each(self.data_base.insert)
    data_sheet.append(new_articles)
    log.info(
      'crawled channel key [{}] finished. # new channel: {}, crawling time: {}'.format(
        channel_key,
        new_articles.size(),
        time.time() -
        context_start_time))

  def crawl(self, min_crawl_page, crawler, start_url):
    new_articles = seq([])
    checked_count = 0

    for i in range(0, self.max_crawl_page):
      if i >= min_crawl_page and checked_count > 0:
        break

      start_index = i * 10 + 1
      url = start_url + '&start={}'.format(start_index)
      articles = crawler.crawl_url(url)
      urls = articles.map(lambda d: d['url']).to_set()
      checked_urls = self.data_base.check_urls(urls)
      checked_count += len(checked_urls)

      new_urls = urls - checked_urls
      new_articles += articles.filter(lambda a: a['url'] in new_urls)
    return new_articles


if __name__ == '__main__':
  processor = CrawlProcessor()
  processor.start()
