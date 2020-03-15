import random
import re
import time
from datetime import datetime
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from functional import seq

from definitions import log


class NaverCrawler:
  def __init__(self, sleep_time=3):
    self.sleep_time = sleep_time

  def crawl_url(self, url):
    time.sleep(self.sleep_time + random.random())

    log.info('start to crawl from url: {}'.format(url))
    page_html = requests.get(url).text
    soup = BeautifulSoup(page_html, 'html.parser')
    return self.parse_soup(soup)

  def parse_soup(self, soup):
    article_list = soup.find('ul', class_='type01')
    return seq(article_list.find_all('li')).map(self.extract_article)

  def extract_article(self, article):
    anchor = article.select('dl > dt > a')[0]
    title = anchor.text
    url = anchor['href']
    article_info_text = article.select('dl > dd.txt_inline')[0]

    poster_node = article_info_text.find('span', class_='_sp_each_source')
    poster = poster_node.text

    num_bars = len(article_info_text.find_all('span', class_='bar'))
    time_str_index = 3
    if num_bars == 4:
      time_str_index = 7

    time_str = list(poster_node.next_siblings)[time_str_index - 1].strip()
    formatted_time = self.format_time(datetime.now(), time_str)
    return {'datetime': formatted_time, 'title': title, 'url': url, 'poster': poster}

  def format_time(self, now, time_str):
    date_format = '%Y-%m-%d %H:%M:%S'
    if '분 전' in time_str:
      minute_before = int(re.compile('(\d+)분 전').search(time_str).group(1))
      return (now - timedelta(minutes=minute_before)).strftime(date_format)
    elif '시간 전' in time_str:
      hour_before = int(re.compile('(\d+)시간 전').search(time_str).group(1))
      return (now - timedelta(hours=hour_before)).strftime(date_format)
    elif '일 전' in time_str:
      day_before = int(re.compile('(\d+)일 전').search(time_str).group(1))
      return (now - timedelta(days=day_before)).strftime(date_format)
    else:
      return datetime.strptime(time_str, '%Y.%m.%d.').strftime(date_format)


if __name__ == '__main__':
  start_url = 'https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EB%A1%9C%EB%82%98&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&mynews=0&refresh_start=0&related=0'

  crawler = NaverCrawler()
  articles = crawler.crawl_url(start_url)
  for i in articles:
    print(i)
