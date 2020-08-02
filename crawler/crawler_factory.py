from crawler import crawler
from crawler.naver_news_parser import NaverNewsParser
from crawler.naver_blog_parser import NaverBlogParser
from crawler.naver_cafe_parser import NaverCafeParser
from crawler.naver_realtime_parser import NaverRealtimeParser
from crawler.aagag_mirror_parser import AagagMirrorParser

naver_news_crawler = crawler.Crawler('네이버뉴스', NaverNewsParser(), '네이버', '뉴스')
naver_blog_crawler = crawler.Crawler('네이버블로그', NaverBlogParser(), '네이버', '블로그')
naver_cafe_crawler = crawler.Crawler('네이버카페', NaverCafeParser(), '네이버', '카페')
naver_realtime_crawler = crawler.Crawler('네이버실시간검색', NaverRealtimeParser(), '네이버', '실시간검색')

aagag_mirror_parser = crawler.Crawler('기타커뮤니티', AagagMirrorParser(), '기타', '커뮤니티')
