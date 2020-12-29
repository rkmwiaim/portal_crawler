from crawler.naver_common_parser import *


class NaverRealtimeParser:
  def get_article_list(self, soup_root):
    lists = soup_root.find('ul', class_='nrealtime_list')
    if lists is None and soup_root.find('div', class_='not_found02'):
      return []
    else:
      return lists.find_all('li')

  def get_title(self, article_node):
    return self.get_realtime_content(article_node)

  def get_realtime_content(self, article_node):
    return article_node.find(None, class_='desc_txt').text

  def get_url(self, article_node):
    return self.get_realtime_id(article_node)

  def get_realtime_id(self, article_node):
    return article_node.find('a', attrs={'crlink': True})['crlink']

  def get_poster(self, article_node):
    return article_node.find('a', class_='desc_tit').text.strip()

  def get_posted_at(self, article_node):
    time_str = article_node.find(None, class_='detail_time').text
    return format_time(datetime.now(), time_str)

  def post_process(self, article_node, parse_result):
    parse_result['realtime_type'] = self.get_realtime_type(article_node)
    parse_result['realtime_url'] = self.get_realtime_url(article_node)
    parse_result['realtime_post_title'] = self.get_realtime_post_title(article_node)

  def get_realtime_type(self, article_node):
    thumbnail_node = article_node.find(None, class_='item_thumb')
    if 'data-twitter-link' in thumbnail_node.attrs:
      return '트위터'
    else:
      return thumbnail_node.text

  def get_realtime_url(self, article_node):
    if self.get_realtime_type(article_node) == '트위터':
      return article_node.find('div', class_='desc_txt')['data-src']
    else:
      return article_node.find('a', class_='desc_txt')['href']

  def get_realtime_post_title(self, article_node):
    if self.get_realtime_type(article_node) == '트위터':
      return ''
    else:
      return article_node.find('span', class_='source_txt').text
