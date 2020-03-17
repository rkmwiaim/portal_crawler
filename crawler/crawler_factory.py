from crawler import crawler
from crawler.naver_news_parser import NaverNewsParser

naver_news_crawler = crawler.Crawler('네이버뉴스', NaverNewsParser())
