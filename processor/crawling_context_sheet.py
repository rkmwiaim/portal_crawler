from external import spread_sheet_api
from functional import seq

SPREADSHEET_ID = '1se6gCkUgE6kajK_14jpVHPhOAbUt2dQ7aF74Oyw16KE'
CONTEXT_RANGE = '채널!A2:G'


def get_channel_key(portal, channel):
  return portal + channel


class CrawlingContextSheet(spread_sheet_api.SpreadSheetApi):
  def __init__(self):
    super().__init__(SPREADSHEET_ID)

  def get(self):
    rows = super().get(CONTEXT_RANGE)
    return seq(rows).map(lambda row: {
      'portal': row[0],
      'channel': row[1],
      'spreadsheet_id': row[2],
      'tab_name': row[3],
      'crawl_page': row[4],
      'start_cell': row[5],
      'start_url': row[6]
    }).filter(lambda d: len(d['spreadsheet_id']) > 0)\
      .map(lambda d: (get_channel_key(d['portal'], d['channel']), d))\
      .to_dict()


if __name__ == '__main__':
  context_sheet = CrawlingContextSheet()
  contexts = context_sheet.get()
  for c in contexts:
    print(c)
