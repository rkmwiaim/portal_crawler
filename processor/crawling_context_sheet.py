from typing import Dict

from external import spread_sheet_api
from functional import seq
from processor.processor_util import get_channel_key

SPREADSHEET_ID = '1se6gCkUgE6kajK_14jpVHPhOAbUt2dQ7aF74Oyw16KE'
CONTEXT_RANGE = '채널!A2:I'


class CrawlingContextSheet(spread_sheet_api.SpreadSheetApi):
  def __init__(self):
    super().__init__(SPREADSHEET_ID)

  def get(self) -> Dict[str, dict]:
    rows = super().get(CONTEXT_RANGE)
    return seq(rows).map(self.transform_row)\
      .filter(lambda d: len(d['spreadsheet_id']) > 0) \
      .map(lambda d: (get_channel_key(d['portal'], d['channel']), d)) \
      .group_by_key() \
      .to_dict()

  def transform_row(self, row) -> dict:
    keyword = row[8] if len(row) >= 9 else ''
    return {
      'portal': row[0],
      'channel': row[1],
      'spreadsheet_id': row[2],
      'tab_name': row[3],
      'crawl_page': row[4],
      'start_cell': row[5],
      'start_url': row[6],
      'keyword': keyword
    }


if __name__ == '__main__':
  context_sheet = CrawlingContextSheet()
  contexts = context_sheet.get()
  for c in contexts:
    print(c)
