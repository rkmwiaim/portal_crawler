import os
import random
import time
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from functional import seq

import config
import definitions
import external.telegram_bot as bot
from definitions import log
from models.types import Stream


class Crawler:
  def __init__(self, name, parser, site, channel):
    self.name = name
    self.sleep_time = config.PAGE_CRAWL_TIME_GAP
    self.parser = parser
    self.site = site
    self.channel = channel

  def crawl_url(self, url) -> Stream[dict]:
    time.sleep(self.sleep_time + random.random())
    log.info('start to crawl from url: {}'.format(url))

    page_html = requests.get(url).text
    try:
      root_node = BeautifulSoup(page_html, 'html.parser')
      return self.parse_soup(root_node).cache()
    except:
      self.handle_parse_error(page_html, url)

  def parse_soup(self, soup) -> Stream[dict]:
    article_list = self.parser.get_article_list(soup)
    articles = seq(article_list).map(self.parse_article).cache()
    if getattr(self.parser, "filter_article", None):
      return articles.filter(self.parser.filter_article)
    else:
      return articles

  def parse_article(self, article_node) -> dict:
    title = self.parser.get_title(article_node)
    url = self.parser.get_url(article_node)
    poster = self.parser.get_poster(article_node)
    posted_at = self.parser.get_posted_at(article_node)

    parse_result = {'title': title, 'url': url, 'poster': poster,
                    'posted_at': posted_at, 'site': self.site, 'channel': self.channel}
    if getattr(self.parser, "post_process", None):
      self.parser.post_process(article_node, parse_result)

    return parse_result

  def handle_parse_error(self, page_html, url):
    log.error('failed to parse {}'.format(url))
    error_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    error_html_file_path = os.path.join(definitions.ERROR_FILE_DIR, '{}.html'.format(error_datetime))
    with open(error_html_file_path, 'w') as f:
      f.write(page_html)
    traces = traceback.format_exc()
    error_trace_file_path = os.path.join(definitions.ERROR_FILE_DIR, '{}.log'.format(error_datetime))
    with open(error_trace_file_path, 'w') as f:
      f.write(traces)
    bot.send_message(bot.telegram_ids['error_log'], f'Error from [portal_crawler]. failed to parse url: {url}')
    raise
