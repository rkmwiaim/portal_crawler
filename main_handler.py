import argparse

from definitions import log
from handler import naver_blog_handler
from models.crawler_arguments import CrawlerArgs

MAX_CRAWL_PAGE = 100
PAGE_CRAWL_TIME_GAP = 3

parser = argparse.ArgumentParser()
parser.add_argument('--portal', help='포털 이름 (한글). ex) 네이버')
parser.add_argument('--channel', help='채널 이름 (한글). ex) 뉴스')
parser.add_argument('--max_page', type=int, required=False, help='최대 crawling 할 페이지 수', default=MAX_CRAWL_PAGE)
parser.add_argument('--sleep', type=int, required=False, help='페이지 crawling 마다 sleep 하는 시간 (초)',
                    default=PAGE_CRAWL_TIME_GAP)
args = parser.parse_args()

HANDLER_KEY_DELEMETER = '^'

handlers = {
    f'네이버{HANDLER_KEY_DELEMETER}블로그': naver_blog_handler
}


def create_handler_key(portal, channel):
    return f'{portal}{HANDLER_KEY_DELEMETER}{channel}'


def get_handler(portal, channel):
    key = create_handler_key(portal, channel)
    return handlers[key]


def main():
    log.info(f'args: {vars(args)}')

    portal = args.portal
    channel = args.channel

    handler = get_handler(portal, channel)
    crawler_args = CrawlerArgs(portal, channel, args.max_page, args.sleep)
    handler.handle(crawler_args)


if __name__ == '__main__':
    main()
