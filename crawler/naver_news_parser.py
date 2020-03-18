from crawler.naver_common_parser import *


class NaverNewsParser:
  def get_article_list(self, soup_root):
    return get_article_list(soup_root)

  def get_title(self, article_node):
    return get_title(article_node)

  def get_url(self, article_node):
    return get_url(article_node)

  def get_poster(self, article_node):
    return self.get_poster_node(article_node).text

  def get_posted_at(self, article_node):
    info = self.get_article_info(article_node)
    num_bars = len(info.find_all('span', class_='bar'))
    time_str_index = 3
    if num_bars == 4:
      time_str_index = 7

    time_str = list(info.children)[time_str_index].strip()
    return format_time(datetime.now(), time_str)

  def get_anchor(self, article_node):
    return get_anchor(article_node)

  def get_article_info(self, article_node):
    return article_node.select('dl > dd.txt_inline')[0]

  def get_poster_node(self, article_node):
    return self.get_article_info(article_node).find('span', class_='_sp_each_source')
