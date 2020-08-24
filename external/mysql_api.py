import os
from typing import List

import pymysql
import yaml
from functional import seq
import definitions
from datetime import datetime
import json

with open(os.path.join(definitions.RESOURCE_DIR, 'mysql_conf.yaml')) as f:
    MYSQL_CONF = yaml.load(f, Loader=yaml.FullLoader)


def update(sql):
    conn = get_conn()
    try:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()
        return curs.lastrowid
    finally:
        conn.close()


def select(sql) -> List[dict]:
    conn = get_conn()
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(sql)
        return curs.fetchall()
    finally:
        conn.close()


def insert(article):
    article = seq(article.items()).map(lambda t: (t[0], t[1].replace("'", "''"))).to_dict()
    now = datetime.now().strftime(definitions.TIME_FORMAT)

    sql = f"""INSERT INTO 
                article (site, channel, title, url, poster, posted_at, inserted_at, json) 
                VALUES (
                  '{article['site']}',
                  '{article['channel']}',
                  '{article['title']}',
                  '{article['url']}',
                  '{article['poster']}',
                  '{article['posted_at']}',
                  '{now}',
                  '{json.dumps(article)}')
  """

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
                           db=MYSQL_CONF['db'], charset='utf8mb4')


if __name__ == '__main__':
    # 'poster': '⚡️전기팔이소년⚡️',
    a = {
        'title': "  '코로나19' 비상 속 군산보건소 상황실 전화 1시간 '먹통'",
        'url': 'test_url3',

        'poster': '⚡️전기팔이소년⚡️',
        'posted_at': '2020-03-18 00:54:00',
        'site': 'test',
        'channel': 'test'
    }
    insert(a)
    # r = select_all()
    # print(r)
