from functional import seq

from definitions import log
from models.types import Stream


def crawl(crawler_args, context) -> Stream[dict]:
    new_articles = seq([])

    for i in range(0, crawler_args['max_crawl_page']):
        start_index = i * 10 + 1
        url = context['start_url'] + '&start={}'.format(start_index)
        articles = context['crawler'].crawl_url(url)

        articles = articles.map(lambda a: post_crawl(a, context)).cache()

        if articles.size() == 0:
            continue

        curr_page_new_articles = context['data_base'].filter_non_exist(articles)
        log.info(f'# new articles in page: {curr_page_new_articles.size()}')

        new_articles += curr_page_new_articles

        if i >= (context['min_crawl_page'] - 1) and curr_page_new_articles.size() == 0:
            break

    return new_articles


def post_crawl(article, context):
    article['keyword'] = context['keyword']
    article['serial_prefix'] = context['serial_prefix']
    return article