import re
from datetime import datetime, timedelta
from definitions import log

class NaverNewsParser:
  def get_article_list(self, soup_root):
    return soup_root.find('ul', class_='type01').find_all('li')

  def get_title(self, article_node):
    return self.get_anchor(article_node).text

  def get_url(self, article_node):
    return self.get_anchor(article_node)['href']

  def get_poster(self, article_node):
    return self.get_poster_node(article_node).text

  def get_posted_at(self, article_node):
    info = self.get_article_info(article_node)
    num_bars = len(info.find_all('span', class_='bar'))
    time_str_index = 3
    if num_bars == 4:
      time_str_index = 7

    time_str = list(info.children)[time_str_index].strip()
    now = datetime.now()
    formatted_time = self.format_time(now, time_str)
    log.info(f"now: {now}, time string: {time_str}, formatted: {formatted_time}")
    return formatted_time

  def get_anchor(self, article_node):
    return article_node.select('dl > dt > a')[0]

  def get_article_info(self, article_node):
    return article_node.select('dl > dd.txt_inline')[0]

  def get_poster_node(self, article_node):
    return self.get_article_info(article_node).find('span', class_='_sp_each_source')

  def format_time(self, now, time_str):
    date_format = '%Y-%m-%d %H:%M:%S'
    if '분 전' in time_str:
      minute_before = int(re.compile('(\d+)분 전').search(time_str).group(1))
      return (now - timedelta(minutes=minute_before)).strftime(date_format)
    elif '시간 전' in time_str:
      hour_before = int(re.compile('(\d+)시간 전').search(time_str).group(1))
      return (now - timedelta(hours=hour_before)).strftime(date_format)
    elif '일 전' in time_str:
      day_before = int(re.compile('(\d+)일 전').search(time_str).group(1))
      return (now - timedelta(days=day_before)).strftime(date_format)
    else:
      return datetime.strptime(time_str, '%Y.%m.%d.').strftime(date_format)
