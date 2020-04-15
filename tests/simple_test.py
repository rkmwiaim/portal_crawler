from bs4 import BeautifulSoup

from crawler import crawler_factory, naver_common_parser
from datetime import datetime
import requests
from crawler.naver_realtime_parser import NaverRealtimeParser
from functional import seq

if __name__ == '__main__':
  # url = 'https://search.naver.com/search.naver?where=realtime&query=%EC%BD%94%EB%A1%9C%EB%82%98&ie=utf8&sm=tab_opt&section=22&best=0&mson=0'
  # # url = 'https://search.naver.com/search.naver?where=realtime&query=%EC%BD%94%EB%A1%9C%EB%82%98&ie=utf8&sm=tab_opt&section=6&best=0&mson=0'
  # page_html = requests.get(url).text
  # soup = BeautifulSoup(page_html, 'html.parser')
  # parser = NaverRealtimeParser()
  # article_list = parser.get_article_list(soup)
  # for a in article_list:
  #   print(parser.get_realtime_url(a))

  urls = []
  articles = seq(range(10))
  channel_key = 'abc'
  print(f"crawled new [{channel_key}] articles. #articles: {articles.size()}\n{urls}")
