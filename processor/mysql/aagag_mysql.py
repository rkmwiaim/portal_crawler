import json
from datetime import datetime

from functional import seq

import definitions
from external import mysql_api


def insert(article):
    article = seq(article.items()).map(lambda t: (t[0], t[1].replace("'", "''"))).to_dict()
    now = datetime.now().strftime(definitions.TIME_FORMAT)

    sql = f"""INSERT INTO 
                aagag (title, url, poster, posted_at, inserted_at, community, json) 
                VALUES (
                  '{article['title']}',
                  '{article['url']}',
                  '{article['poster']}',
                  '{article['posted_at']}',
                  '{article['community']}',
                  '{now}',
                  '{json.dumps(article)}')
  """

    return mysql_api.update(sql)


def filter_non_exist(urls) -> list:
    joined_url = ','.join(seq(urls).map(lambda s: f"'{s}'"))
    sql = f"SELECT url FROM aagag WHERE url IN ({joined_url})"
    return seq(mysql_api.select(sql)).map(lambda d: d['url']).set()


if __name__ == '__main__':
    a = {
        'title': "  '코로나19' 비상 속 군산보건소 상황실 전화 1시간 '먹통'",
        'url': 'test_url3',

        'poster': '⚡️전기팔이소년⚡️',
        'posted_at': '2020-03-18 00:54:00',
        'site': 'test',
        'channel': 'test'
    }
    r = insert(a)
    print(r)
