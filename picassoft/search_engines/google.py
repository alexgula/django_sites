# coding=utf-8
from .base_grab import GrabEngine


class GoogleEngine(GrabEngine):

    verbose_name = u"Google"
    captcha_selector = '//*[@id = "captcha"]'

    def __init__(self, log_file='google.html', address='http://google.com.ua/', *args, **kwargs):
        super(GoogleEngine, self).__init__(log_file, address, *args, **kwargs)

    def search_setup(self, query):
        self.crawler.go(self.address)
        self.crawler.set_input('q', query)
        self.crawler.submit()

    def page_search(self):
        for li in self.crawler.css_list('#ires .g'):
            if li not in self.crawler.css_list('#imagebox_bigimages'):
                if li.find('table') is None: # Got no table with Google ads.
                    yield li.cssselect('a')[0].attrib.get('href', '')

    def next_page(self):
        page = self.crawler.css('.b a').attrib.get('href')
        self.crawler.go(page)
