from crawler.naver_common_parser import *


class NaverNewsParser:
    def get_article_list(self, soup_root):
        return soup_root.find('ul', class_='list_news').find_all('li')

    def get_news_anchor(self, article_node):
        return article_node.find('a', class_='news_tit')

    def get_title(self, article_node):
        return self.get_news_anchor(article_node).text

    def get_url(self, article_node):
        return self.get_news_anchor(article_node)['href']

    def get_poster(self, article_node):
        return str(article_node.find('a', class_='press').find(text=True, recursive=False))

    def get_posted_at(self, article_node):
        info_nodes = article_node.find('div', class_='info_group').find_all('span', class_='info')
        if len(info_nodes) == 2:
            time_str = info_nodes[1].text
        else:
            time_str = info_nodes[0].text
        return format_time(datetime.now(), time_str)

    def get_article_info(self, article_node):
        return article_node.select('dl > dd.txt_inline')[0]

    def get_poster_node(self, article_node):
        return self.get_article_info(article_node).find('span', class_='_sp_each_source')

    def post_process(self, article_node, parse_result):
        self.set_news_type(article_node, parse_result)
        self.set_naver_news_url(article_node, parse_result)

    def set_news_type(self, article_node, parse_result):
        thumbnail_node = article_node.find('a', class_='dsc_thumb')
        if thumbnail_node is not None:
            if 'type_video' in thumbnail_node['class']:
                parse_result['type'] = 'video'

    def set_naver_news_url(self, article_node, parse_result):
        naver_news_anchor = article_node.find('a', class_='info', string='네이버뉴스')
        if naver_news_anchor is not None:
            parse_result['naver_news_url'] = naver_news_anchor['href']
