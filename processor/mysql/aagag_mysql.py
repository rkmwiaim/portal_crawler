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
    escaped_articles = seq(articles).map(mysql_util.escape_single_quote)
    joined = ','.join(escaped_articles.map(article_to_tuple))
    sql = f"SELECT * FROM aagag WHERE (title, poster, posted_at, community, keyword) IN ({joined})"

    crawled_key_dict = articles.map(lambda a: (article_to_tuple(a), a)).dict()
    old_key_dict = seq(mysql_api.select(sql)).map(lambda a: (article_to_tuple(a), a)).dict()

    new_keys = crawled_key_dict.keys() - old_key_dict.keys()
    return seq(crawled_key_dict.items()).filter(lambda t: t[0] in new_keys).map(lambda t: t[1])


if __name__ == '__main__':
    sql = "SELECT * FROM aagag WHERE (title, poster, posted_at, community, keyword) IN ((\'서민 \'\'세월호 사건 선동\'\'\', \'라쿠니\', \'2020-08-31 12:07:00\', \'lien\', \'유벙언\'))"
    sql = "SELECT * FROM aagag WHERE title like '서민 %'"
    sql = "SELECT * FROM aagag WHERE title='서민 ''세월호 사건 선동''';"
    # sql = "SELECT * FROM aagag WHERE poster='라쿠니'"
    r = mysql_api.select(sql)
    print(r)
    print(len(r))


