import re
from datetime import datetime, timedelta
from definitions import log
from crawler.naver_common_parser import *


class NaverBlogParser:
  def get_article_list(self, soup_root):
    return get_article_list(soup_root)

  def get_title(self, article_node):
    return get_title(article_node)

  def get_url(self, article_node):
    return get_url(article_node)

  def get_poster(self, article_node):
    return article_node.select('dl > dd.txt_block > span > a.txt84')[0]['href']

  def get_posted_at(self, article_node):
    time_str = article_node.select('dl > dd.txt_inline')[0].text
    return format_time(datetime.now(), time_str)
