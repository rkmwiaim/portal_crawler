import os
import unittest

from bs4 import BeautifulSoup

from crawler.crawler_factory import naver_news_crawler
import definitions


class CrawlerTest(unittest.TestCase):

  def test_parse_naver_news(self):
    test_file_path = os.path.join(definitions.TEST_RESOURCE_DIR, 'naver_news.htm')
    with open(test_file_path, 'r') as f:
      html = f.read()
      soup = BeautifulSoup(html, 'html.parser')
      articles = naver_news_crawler.parse_soup(soup)
      self.assertEqual(articles.size(), 10)


if __name__ == '__main__':
  unittest.main()
