from external.big_query_api import BigQueryApi
from functional import seq
from datetime import datetime

COUNT_QUERY = """SELECT count(url) as url_count FROM `portal_data.crawled_data` WHERE url='{}'"""
URL_CHECK_QUERY = """SELECT url FROM `portal_data.crawled_data` WHERE url IN ({})"""

INSERT_QUERY = """INSERT INTO `portal_data.crawled_data` (datetime, poster, title, url) 
                  VALUES ('{}', '{}', '{}', '{}') """

DELETE_QUERY = """DELETE FROM `portal_data.crawled_data` WHERE url='{}'"""


class CrawlerDataBase:
  def __init__(self):
    self.bigquery_api = BigQueryApi()

  def check_urls(self, urls):
    url_list_str = ','.join(seq(urls).map(lambda s: "'{}'".format(s)))
    results = self.bigquery_api.query(
      URL_CHECK_QUERY.format(url_list_str))

    return seq(results).map(lambda r: r.url).to_set()

  def insert(self, article):
    def remove_quote(article):
      return seq(article.items()).map(lambda t: (t[0], t[1].replace("'", '"'))).to_dict()

    preprocessed = remove_quote(article)
    self.bigquery_api.query(INSERT_QUERY.format(
      preprocessed['datetime'],
      preprocessed['poster'],
      preprocessed['title'],
      preprocessed['url']
    ))

  def delete(self, data):
    self.bigquery_api.query(DELETE_QUERY.format(data['url']))


if __name__ == '__main__':
  data_base = CrawlerDataBase()

  # d = {
  #   'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
  #   'poster': '연합뉴스',
  #   'title': "코로나19에 대형교회들 \'온라인 예배\'…일부는 현장예배 강행",
  #   'url': 'http://yna.kr/AKR20200315027400004?did=1195m'
  # }
  # data_base.insert(d)

  # data_base.delete(d)

  # checked_urls = data_base.check_urls(['test_url', 'test_url2', 'a', 'b'])
  # print(checked_urls)
  # data_base.bigquery_api.query("DELETE FROM `portal_data.crawled_data`")
