from crawler import crawler_factory, naver_common_parser
from datetime import datetime

if __name__ == '__main__':
  date_str = '2020.04.06. '
  result = naver_common_parser.format_time(datetime.now(), date_str)
  print(result)
