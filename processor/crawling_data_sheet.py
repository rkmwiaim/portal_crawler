import definitions
from external import spread_sheet_api
import processor.spread_sheet_util as spread_sheet_util
from processor.processor_util import get_channel_key
import datetime

class CrawlingDataSheet(spread_sheet_api.SpreadSheetApi):
  def __init__(self, context):
    super().__init__(context['spreadsheet_id'])
    self.context = context
    self.tab_name = context['tab_name']
    start_cell = context['start_cell']
    self.range = '{}!{}'.format(self.tab_name, self.add_column(start_cell))

  def add_column(self, a1_notation):
    col, row = spread_sheet_util.split_A1_notation(a1_notation)
    added_col = spread_sheet_util.col2num(col) + 1
    return spread_sheet_util.num2col(added_col) + row

  def append(self, articles):
    data = articles.map(self.transform_article).to_list()
    return super().append(self.range, data)

  def transform_article(self, a):
    transformed = self.transform_article_default(a)
    channel_key = get_channel_key(self.context['portal'], self.context['channel'])

    if channel_key == '네이버뉴스':
      transformed = self.transform_naver_news(transformed, a)
    if channel_key == '네이버실시간검색':
      transformed = self.transform_naver_realtime(transformed, a)
    if channel_key == '커뮤니티AAGAG':
      transformed = self.transform_aagag(transformed, a)

    if channel_key != '커뮤니티AAGAG':
     self.post_transform(a, transformed)
    return transformed

  def post_transform(self, article, transformed):
    inserted_at = article['inserted_at']
    serial_number = self.get_serial_number(article)
    transformed.append(inserted_at)
    transformed.append(serial_number)

  def get_serial_number(self, article):
    serial_prefix = article['serial_prefix']
    yymm = datetime.datetime.strptime(article['posted_at'], definitions.TIME_FORMAT).strftime('%y%m')
    id_number = str(article["id"]).zfill(7)
    return f'{serial_prefix}_{yymm}_{id_number}'

  def transform_article_default(self, a):
    return ['', a['posted_at'], a['poster'], a['title'], a['url']]

  def transform_naver_news(self, transformed, a):
    transformed.append(a.get('naver_news_url', ''))
    transformed.append(a.get('type', ''))

    return transformed

  def transform_naver_realtime(self, transformed, a):
    return ['', a['posted_at'], a['poster'], a['title'], a['realtime_type'], a['realtime_post_title'], a['realtime_url']]

  def transform_aagag(self, transformed, a):
    return [a['id'], a['community'], '', a['posted_at'], a['poster'], '', a['title'], a['url'], a['keyword']]


if __name__ == '__main__':
  c = CrawlingDataSheet({
    'spreadsheet_id': '1se6gCkUgE6kajK_14jpVHPhOAbUt2dQ7aF74Oyw16KE',
    'tab_name': '네이버뉴스',
    'start_cell': 'A2'
  })
  print(c.range)
  from functional import seq

  c.append(seq([{'posted_at': '1', 'poster': '1', 'title': '1', 'url': '1'}]))
