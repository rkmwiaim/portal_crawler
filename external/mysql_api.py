import os

import pymysql
import yaml
from functional import seq
import definitions
from datetime import datetime

with open(os.path.join(definitions.RESOURCE_DIR, 'mysql_conf.yaml')) as f:
  MYSQL_CONF = yaml.load(f, Loader=yaml.FullLoader)


def insert(article):
  article = seq(article.items()).map(lambda t: (t[0], t[1].replace("'", "\\\'"))).to_dict()
  now = datetime.now().strftime(definitions.TIME_FORMAT)

  sql = f"""INSERT INTO 
                article(title, url, poster, posted_at, inserted_at) 
                VALUES('{article['title']}','{article['url']}','{article['poster']}','{article['posted_at']}', {now})"""

  conn = get_conn()
  try:
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()
  finally:
    conn.close()


def check_urls(urls):
  joined_url = ','.join(seq(urls).map(lambda s: f"'{s}'"))
  sql = f"SELECT url FROM article WHERE url IN ({joined_url})"
  conn = get_conn()
  try:
    curs = conn.cursor()
    curs.execute(sql)
    rows = curs.fetchall()
    return seq(rows).map(lambda t: t[0]).to_set()
  finally:
    conn.close()


def select_all():
  with get_conn() as cursor:
    sql = "SELECT * FROM article"
    cursor.execute(sql)

    rows = cursor.fetchall()
    return rows


def get_conn():
  return pymysql.connect(host=MYSQL_CONF['host'],
                         port=MYSQL_CONF['port'],
                         user=MYSQL_CONF['user'], password=MYSQL_CONF['password'],
                         db=MYSQL_CONF['db'], charset='utf8')


if __name__ == '__main__':
  a = {
    'title': '\\\'코로나19\\\' 비상 속 군산보건소 상황실 전화 1시간 \\\'먹통\\\'',
    'url': 'test_url3',
    'poster': '테스터',
    'posted_at': '2020-03-18 00:54:00'
  }
  insert(a)
  r = select_all()
  print(r)
  # r = check_urls(set(['test_url', 'test_url2', 'a', 'b']))
  # for i in r:
  #   print(i)
