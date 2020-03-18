import os
import unittest

from bs4 import BeautifulSoup

import definitions
from crawler.crawler_factory import *


class CrawlerTest(unittest.TestCase):

  def test_parse_naver_news(self):
    self.naver_html_test('naver_news.htm', naver_news_crawler)

  def test_parse_naver_blog(self):
    self.naver_html_test('naver_blog.htm', naver_blog_crawler)

  def test_parse_naver_cafe(self):
    self.naver_html_test('naver_cafe.htm', naver_cafe_crawler)

  def naver_html_test(self, test_file_name, crawler):
    test_file_path = os.path.join(definitions.TEST_RESOURCE_DIR, test_file_name)
    with open(test_file_path, 'r') as f:
      html = f.read()
      soup = BeautifulSoup(html, 'html.parser')
      articles = crawler.parse_soup(soup)
      self.assertEqual(articles.size(), 10)

      items = articles.flat_map(lambda d: d.values())
      items.for_each(self.assertIsNotNone)
      string_items = items.filter(lambda i: isinstance(i, str))
      self.assertGreater(string_items.size(), 0)

      string_items.for_each(lambda i: self.assertGreater(len(i), 0))


if __name__ == '__main__':
  unittest.main()
