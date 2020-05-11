from crawler.naver_common_parser import *


class NaverRealtimeParser:
  def get_article_list(self, soup_root):
    lists = soup_root.find('ul', class_='type01')
    if lists is None: return []

    return lists.find_all('li')

  def get_title(self, article_node):
    return self.get_realtime_content(article_node)

  def get_realtime_content(self, article_node):
    return article_node.select('dl > dd:nth-child(2)')[0].text

  def get_url(self, article_node):
    return self.get_realtime_id(article_node)

  def get_realtime_id(self, article_node):
    return article_node.select('div > a')[0]['crlink']

  def get_poster(self, article_node):
    return article_node.find('span', class_='user_name').text

  def get_posted_at(self, article_node):
    timeinfo_node = article_node.find('span', class_='_timeinfo')
    if timeinfo_node is None:
      timeinfo_node = article_node.find('a', class_='_timeinfo')
    time_str = timeinfo_node.text
    return format_time(datetime.now(), time_str)

  def post_process(self, article_node, parse_result):
    parse_result['realtime_type'] = self.get_realtime_type(article_node)
    parse_result['realtime_url'] = self.get_realtime_url(article_node)
    parse_result['realtime_post_title'] = self.get_realtime_post_title(article_node)

  def get_realtime_type(self, article_node):
    thumb_img = article_node.select('div.thumb > a > img')
    type_text = thumb_img[0]['alt']
    if '썸네일' in type_text:
      type_text = '트위터'
    return type_text

  def get_realtime_url(self, article_node):
    content_node = article_node.find('a', class_='txt_link')
    if content_node is None:
      content_node = article_node.find('span', class_='cmmt')
      return content_node['data-src']
    else:
      return content_node['href']

  def get_realtime_post_title(self, article_node):
    post_title_node = article_node.find('a', class_='info_tit')
    if post_title_node is None:
      return ''
    else:
      return post_title_node.text
