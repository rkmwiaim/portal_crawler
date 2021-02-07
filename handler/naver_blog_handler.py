import time

from definitions import log
from main_handler import create_handler_key
from models.crawler_arguments import CrawlerArgs
from processor.crawling_context_sheet import CrawlingContextSheet


def crawl(args: CrawlerArgs):
    context_dict = CrawlingContextSheet().get()
    max_crawl_page = args.max_page
    key = create_handler_key(args.portal, args.channel)

    log.info(f'Processor channel key: {key}, max crawl page: {args.max_page}')

    contexts = context_dict[key]
    for context in contexts:
        context_start_time = time.time()

        log.info('start to crawl channel [{}].'.format(context))

        crawler = crawler_dict[channel_key]
        data_sheet = self.crawling_data_sheet_class(context)
        start_url = context['start_url']
        new_articles = self.crawl(int(context['crawl_page']), crawler, start_url, context)
        new_articles = new_articles.distinct_by(lambda a: a['url']).sorted(key=lambda d: d['posted_at'])

        log.info(f'# total new articles: {new_articles.size()}')

        if new_articles.size() > 0:
            new_articles = new_articles.map(self.data_base.insert).cache()
            data_sheet.append(new_articles)

            self.send_telegram_msg(channel_key, context, new_articles)

        log.info(
            f'crawled channel key [{channel_key}] finished. # new channel: {new_articles.size()}, crawling time: {time.time() - context_start_time}')
    return []


def save(articles):
    pass


def handle(args: CrawlerArgs):
    articles = crawl(args)
    save(articles)
