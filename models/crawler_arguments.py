class CrawlerArgs:
    def __init__(self, portal, channel, max_page, sleep) -> None:
        self.portal = portal
        self.channel = channel
        self.max_page = max_page
        self.sleep = sleep
