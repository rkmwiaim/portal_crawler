import json
from datetime import datetime

from functional import seq

import definitions
from external import mysql_api
from models.types import Stream


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
                  '{now}',
                  '{article['community']}',
                  '{json.dumps(article)}')
  """

    row_id = mysql_api.update(sql)
    article['id'] = row_id
    return article


def article_to_tuple(article):
    title = article['title']
    poster = article['poster']
    posted_at = article['posted_at']
    community = article['community']
    return f"('{title}', '{poster}', '{posted_at}', '{community}')"


def filter_non_exist(articles: Stream[dict]) -> Stream[dict]:
    article_cache = articles.cache()
    joined = ','.join(article_cache.map(article_to_tuple))
    sql = f"SELECT * FROM aagag WHERE (title, poster, posted_at, community) IN ({joined})"

    crawled_key_dict = article_cache.map(lambda a: (article_to_tuple(a), a)).dict()
    old_key_dict = seq(mysql_api.select(sql)).map(lambda a: (article_to_tuple(a), a)).dict()

    new_keys = crawled_key_dict.keys() - old_key_dict.keys()
    return seq(crawled_key_dict.items()).filter(lambda t: t[0] in new_keys).map(lambda t: t[1])



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
