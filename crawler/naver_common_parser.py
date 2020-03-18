import re
from datetime import datetime, timedelta

def get_article_list(soup_root):
  return soup_root.find('ul', class_='type01').find_all('li')


def get_anchor(article_node):
  return article_node.select('dl > dt > a')[0]


def get_title(article_node):
  return get_anchor(article_node).text


def get_url(article_node):
  return get_anchor(article_node)['href']


def get_poster(article_node):
  return article_node.select('dl > dd.txt_block > span > a.txt84')[0]['href']


def get_posted_at(article_node):
  time_str = article_node.select('dl > dd.txt_inline')[0].text
  return format_time(datetime.now(), time_str)


def format_time(now, time_str):
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

