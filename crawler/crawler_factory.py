from crawler import crawler
from crawler.naver_news_parser import NaverNewsParser
from crawler.naver_blog_parser import NaverBlogParser

naver_news_crawler = crawler.Crawler('네이버뉴스', NaverNewsParser())
naver_blog_crawler = crawler.Crawler('네이버블로그', NaverBlogParser())
