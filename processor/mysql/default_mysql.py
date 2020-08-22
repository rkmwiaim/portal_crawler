import json
from datetime import datetime

from functional import seq

import definitions
from external import mysql_api


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

    return mysql_api.update(sql)


def check_urls(urls) -> list:
    joined_url = ','.join(seq(urls).map(lambda s: f"'{s}'"))
    sql = f"SELECT url FROM article WHERE url IN ({joined_url})"
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

    # mysql_api.update("insert into test(a, b, c) values (1, 1, 1);")
    # mysql_api.update("insert into test(a, b, c) values (1, 2, 1);")
    # mysql_api.update("insert into test(a, b, c) values (1, 3, 1);")

    # r = mysql_api.select("SELECT * FROM test")
    # print(r)

    # urls = [
    #     'http://www.ggilbo.com/news/articleView.html?idxno=751540',
    #     'http://goodnews1.com/news/news_view.asp?seq=95427',
    #     'https://www.ksg.co.kr/news/main_newsView.jsp?pNum=125410',
    #     'a'
    # ]
    #
    # r = check_urls(urls)
    # print(r)
