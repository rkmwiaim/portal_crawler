import unittest

from crawler.crawler_factory import *
from tests.test_util import *


class CrawlerTest(unittest.TestCase):

  def test_parse_naver_news(self):
    self.naver_html_test('naver_news.htm', naver_news_crawler)

  def test_parse_naver_news_video(self):
    self.naver_news_post_process_test('naver_news_video.htm', 'video')

  def test_parse_naver_news_newspaper(self):
    self.naver_news_post_process_test('naver_news_newspaper.htm', 'newspaper')

  def test_parse_naver_blog(self):
    self.naver_html_test('naver_blog.htm', naver_blog_crawler)

  def test_parse_naver_cafe(self):
    self.naver_html_test('naver_cafe.htm', naver_cafe_crawler)

  def naver_html_test(self, test_file_name, crawler):
    soup = file_to_soup(test_file_name)
    articles = crawler.parse_soup(soup)
    self.assertEqual(articles.size(), 10)

    items = articles.flat_map(lambda d: d.values())
    items.for_each(self.assertIsNotNone)
    string_items = items.filter(lambda i: isinstance(i, str))
    self.assertGreater(string_items.size(), 0)

    string_items.for_each(lambda i: self.assertGreater(len(i), 0))

  def naver_news_post_process_test(self, test_file_name, type_name):
    soup = file_to_soup(test_file_name)
    articles = naver_news_crawler.parse_soup(soup)
    news_type = articles[0].get('type')
    self.assertIsNotNone(news_type)
    self.assertEqual(news_type, type_name)

if __name__ == '__main__':
  unittest.main()
