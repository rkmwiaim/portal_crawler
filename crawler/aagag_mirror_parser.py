from datetime import datetime

import requests
from bs4 import BeautifulSoup
from functional import seq
import re
import external.url_redirect_follower as url_follower
import definitions

NUM_CRAWL_ARTICLE = 10


class AagagMirrorParser:
    def get_article_list(self, soup_root):
        tables = seq(soup_root.find_all('table', class_='aList'))
        return tables.flat_map(lambda r: r.find_all('a', class_='article')).take(NUM_CRAWL_ARTICLE)

    def get_title(self, article_node):
        title = article_node.find('span', class_='title').text
        return re.sub('\(\d+\)$', '', title)

    def get_url(self, article_node):
        aagag_url = 'https://aagag.com/' + article_node['href']
        redirected_url = url_follower.get_redirected_url(aagag_url)
        if redirected_url is None or len(redirected_url) == 0:
            raise ValueError(f'redirected url is empty. url: {aagag_url}')
        return redirected_url

    def get_poster(self, article_node):
        return article_node.find('span', class_='nick').text

    def get_posted_at(self, article_node):
        posted_at_raw = article_node.find('span', class_='date').text
        posted_at = re.sub('\[.*?\]$', '', posted_at_raw)
        return datetime.strptime(posted_at, '%Y-%m-%d %H:%M').strftime(definitions.TIME_FORMAT)

    def post_process(self, article_node, parse_result: dict):
        community_name = seq(article_node.find('div', class_='rank')['class'])\
            .find(lambda c: c.startswith('bc_'))\
            .strip('bc_')
        parse_result['community'] = community_name

if __name__ == '__main__':
    parser = AagagMirrorParser()
    url = 'https://aagag.com/mirror/?orderby=time&word=%EC%9C%A0%EB%B3%91%EC%96%B8'

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    articles = parser.get_article_list(soup)
    articles.take(3).map(lambda a: parser.post_process(a, {})).for_each(print)
