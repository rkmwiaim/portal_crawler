from crawler.naver_common_parser import *


class NaverBlogParser:
  def get_article_list(self, soup_root):
    return soup_root.find('ul', class_='lst_total').find_all('li')

  def get_blog_anchor(self, article_node):
    return article_node.find('a', class_='total_tit')

  def get_title(self, article_node):
    return self.get_blog_anchor(article_node).text

  def get_url(self, article_node):
    return self.get_blog_anchor(article_node)['href']

  def get_poster(self, article_node):
    return article_node.find('a', class_='sub_name').text

  def get_posted_at(self, article_node):
    time_str = article_node.find('span', class_='sub_time').text
    return format_time(datetime.now(), time_str)
