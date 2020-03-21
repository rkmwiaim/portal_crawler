import unittest
from datetime import datetime

from crawler.crawler_factory import *
from tests.test_util import *
from functional import seq
import crawler.naver_common_parser as naver_common_parser


class ParserTest(unittest.TestCase):

  def test_parse_naver_news(self):
    self.naver_html_test('naver_news.htm', naver_news_crawler)

  def test_parse_naver_news_date(self):
    soup = file_to_soup('naver_news_for_time_str_test.htm')
    articles = naver_news_crawler.parse_soup(soup)
    articles.for_each(lambda a: self.assertIsNotNone(a.get('posted_at')))

  def test_parse_naver_news_video(self):
    self.naver_news_post_process_test('naver_news_video.htm', 'video')

  def test_parse_naver_news_newspaper(self):
    self.naver_news_post_process_test('naver_news_newspaper.htm', 'newspaper')

  def test_parse_naver_news_url(self):
    soup = file_to_soup('naver_news_for_time_str_test.htm')
    articles = naver_news_crawler.parse_soup(soup)

    self.assertIsNone(articles[0].get('naver_news_url'))
    self.assertIsNotNone(articles[1].get('naver_news_url'))
    self.assertIsNotNone(articles[2].get('naver_news_url'))

  def test_parse_naver_blog(self):
    self.naver_html_test('naver_blog.htm', naver_blog_crawler)

  def test_parse_naver_cafe(self):
    self.naver_html_test('naver_cafe.htm', naver_cafe_crawler)

  def test_parse_naver_date_common(self):
    test_date_str = seq([
      '어제',
      '3분 전',
      '3시간 전',
      '3일 전',
      '2020.03.21.'
    ])
    test_date_str\
      .map(lambda dt: naver_common_parser.format_time(datetime.now(), dt))\
      .for_each(lambda s: self.assertIsNotNone(s) and self.assertGreater(len(s), 0))

  ##################################################################################################################

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
