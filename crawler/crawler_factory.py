from crawler import crawler
from crawler.naver_news_parser import NaverNewsParser
from crawler.naver_blog_parser import NaverBlogParser
from crawler.naver_cafe_parser import NaverCafeParser
from crawler.naver_realtime_parser import NaverRealtimeParser

naver_news_crawler = crawler.Crawler('네이버뉴스', NaverNewsParser())
naver_blog_crawler = crawler.Crawler('네이버블로그', NaverBlogParser())
naver_cafe_crawler = crawler.Crawler('네이버카페', NaverCafeParser())
naver_realtime_crawler = crawler.Crawler('네이버실시간검색', NaverRealtimeParser())
