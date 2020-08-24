import time

from functional import seq

import config
import external.telegram_bot as bot
from crawler import crawler_factory
from definitions import log
from processor.mysql import database_factory
from processor.processor_util import get_channel_key
from processor.crawling_context_sheet import CrawlingContextSheet
from processor.crawling_data_sheet import CrawlingDataSheet
from models.types import Stream


crawler_dict = {
  '네이버뉴스': crawler_factory.naver_news_crawler,
  '네이버블로그': crawler_factory.naver_blog_crawler,
  '네이버카페': crawler_factory.naver_cafe_crawler,
  '네이버실시간검색': crawler_factory.naver_realtime_crawler,
  '기타커뮤니티': crawler_factory.aagag_mirror_parser
}


class CrawlProcessor:
  def __init__(self, portal, channel,
               crawling_context_sheet_class=CrawlingContextSheet,
               crawling_data_sheet_class=CrawlingDataSheet):
    context_dict = crawling_context_sheet_class().get()
    self.max_crawl_page = config.MAX_CRAWL_PAGE
    channel_key = get_channel_key(portal, channel)

    self.crawling_data_sheet_class = crawling_data_sheet_class
    self.data_base = database_factory.get(channel_key)

    log.info(f'Processor channel key: {channel_key}, max crawl page: {self.max_crawl_page}')

    self.crawler = crawler_dict.get(channel_key)
    self.contexts = context_dict.get(channel_key)

    self.check_init()

  def check_init(self):
    if self.crawler is None:
      raise ValueError(f'Crawler has yet defined.')

    if self.contexts is None or len(self.contexts) == 0:
      raise ValueError(f'context has yet defined.')

  def start(self):
    for context in self.contexts:
      self.process_context(context)

  def process_context(self, context):
    context_start_time = time.time()

    channel_key = get_channel_key(context['portal'], context['channel'])
    log.info('start to crawl channel [{}].'.format(context))

    crawler = crawler_dict[channel_key]
    data_sheet = self.crawling_data_sheet_class(context)
    start_url = context['start_url']
    new_articles = self.crawl(int(context['crawl_page']), crawler, start_url)
    new_articles = new_articles.distinct_by(lambda a: a['url']).sorted(key=lambda d: d['posted_at'])

    log.info(f'# total new articles: {new_articles.size()}')

    if new_articles.size() > 0:
      new_articles = new_articles.map(self.data_base.insert).cache()
      data_sheet.append(new_articles)

      self.send_telegram_msg(channel_key, context, new_articles)

    log.info(
      f'crawled channel key [{channel_key}] finished. # new channel: {new_articles.size()}, crawling time: {time.time() - context_start_time}')

  def send_telegram_msg(self, channel_key, context, new_articles):
    telegram_group = bot.telegram_ids[channel_key]
    if telegram_group is not None:
      if channel_key == '네이버실시간검색':
        new_articles.for_each(lambda a: self.send_realtime_msg(telegram_group, a))
      else:
        msg = self.get_message(context, new_articles)
        bot.send_message(telegram_group, msg)

  def send_realtime_msg(self, telegram_group, article):
    realtime_type = article['realtime_type']
    poster = article['poster']
    title = article['title']

    msg = f'[{realtime_type}]\n{poster} : {title}'
    bot.send_message(telegram_group, msg)

  def crawl(self, min_crawl_page, crawler, start_url) -> Stream[dict]:
    new_articles = seq([])

    for i in range(0, self.max_crawl_page):
      start_index = i * 10 + 1
      url = start_url + '&start={}'.format(start_index)
      articles = crawler.crawl_url(url)

      if articles.size() == 0:
        continue

      curr_page_new_articles = self.data_base.filter_non_exist(articles)
      log.info(f'# new articles in page: {curr_page_new_articles.size()}')

      new_articles += curr_page_new_articles

      if i >= (min_crawl_page - 1) and curr_page_new_articles.size() == 0:
        break

    return new_articles

  def get_message(self, context, articles):
    channel_key = get_channel_key(context['portal'], context['channel'])
    urls = '\n'.join(articles.map(lambda d: d['url']).to_list())

    return f"crawled new [{channel_key}] articles. num articles: {articles.size()}\n{urls}"
