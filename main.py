import argparse
from processor.crawl_processor import CrawlProcessor
from definitions import log
import config

parser = argparse.ArgumentParser()
parser.add_argument('--portal', help='포털 이름 (한글). ex) 네이버')
parser.add_argument('--channel', help='채널 이름 (한글). ex) 뉴스')
parser.add_argument('--max_page', type=int, required=False, help='최대 crawling 할 페이지 수', default=config.MAX_CRAWL_PAGE)
parser.add_argument('--sleep', type=int, required=False, help='페이지 crawling 마다 sleep 하는 시간 (초)', default=config.PAGE_CRAWL_TIME_GAP)
args = parser.parse_args()

if __name__ == '__main__':
  log.info(f'args: {vars(args)}')

  portal = args.portal
  channel = args.channel

  config.MAX_CRAWL_PAGE = args.max_page
  config.PAGE_CRAWL_TIME_GAP = args.sleep

  crawl_processor = CrawlProcessor(portal, channel)
  crawl_processor.start()
