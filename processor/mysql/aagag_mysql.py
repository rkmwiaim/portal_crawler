import json
from datetime import datetime

from functional import seq

import definitions
from external import mysql_api
from models.types import Stream
from processor.mysql import mysql_util


def insert(article: dict):
    article = mysql_util.escape_single_quote(article)
    now = datetime.now().strftime(definitions.TIME_FORMAT)

    sql = f"""INSERT INTO 
                aagag (title, url, poster, posted_at, inserted_at, community, keyword, json) 
                VALUES (
                  '{article['title']}',
                  '{article['url']}',
                  '{article['poster']}',
                  '{article['posted_at']}',
                  '{now}',
                  '{article['community']}',
                  '{article['keyword']}',
                  '{json.dumps(article)}')
  """

    row_id = mysql_api.update(sql)
    article['id'] = row_id
    article['inserted_at'] = now
    return article


def article_to_tuple(article):
    title = article['title']
    poster = article['poster']
    posted_at = article['posted_at']
    community = article['community']
    keyword = article['keyword']
    return f"('{title}', '{poster}', '{posted_at}', '{community}', '{keyword}')"


def filter_non_exist(articles: Stream[dict]) -> Stream[dict]:
    articles = seq(articles).map(mysql_util.escape_single_quote).cache()
    joined = ','.join(articles.map(article_to_tuple))
    sql = f"SELECT * FROM aagag WHERE (title, poster, posted_at, community, keyword) IN ({joined})"

    crawled_key_dict = articles.map(lambda a: (article_to_tuple(a), a)).dict()
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
