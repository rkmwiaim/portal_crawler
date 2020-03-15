from external import spread_sheet_api
import processor.spread_sheet_util as spread_sheet_util


class CrawlingDataSheet(spread_sheet_api.SpreadSheetApi):
  def __init__(self, context):
    super().__init__(context['spreadsheet_id'])
    self.tab_name = context['tab_name']
    start_cell = context['start_cell']
    self.range = '{}!{}'.format(self.tab_name, self.add_column(start_cell))

  def add_column(self, a1_notation):
    col, row = spread_sheet_util.split_A1_notation(a1_notation)
    added_col = spread_sheet_util.col2num(col) + 1
    return spread_sheet_util.num2col(added_col) + row

  def append(self, article):
    data = article.map(lambda a: ('', a['datetime'], a['poster'], a['title'], a['url'])).to_list()
    return super().append(self.range, data)


if __name__ == '__main__':
  c = CrawlingDataSheet({
    'spreadsheet_id': '1se6gCkUgE6kajK_14jpVHPhOAbUt2dQ7aF74Oyw16KE',
    'tab_name': '네이버뉴스',
    'start_cell': 'A2'
  })
  print(c.range)
  from functional import seq
  c.append(seq([{'datetime': '1', 'poster': '1', 'title': '1', 'url': '1'}]))
