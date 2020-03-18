from crawler.naver_common_parser import *


class NaverCafeParser:
  def get_article_list(self, soup_root):
    return get_article_list(soup_root)

  def get_title(self, article_node):
    return get_title(article_node)

  def get_url(self, article_node):
    return get_url(article_node)

  def get_poster(self, article_node):
    return get_poster(article_node)

  def get_posted_at(self, article_node):
    return get_posted_at(article_node)
