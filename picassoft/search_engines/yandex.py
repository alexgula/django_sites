# coding=utf-8
from .base_grab import GrabEngine


class YandexEngine(GrabEngine):

    verbose_name = u"Yandex"
    captcha_selector = '//*[@class = "b-captcha"]'

    def __init__(self, log_file='yandex.html', address='http://yandex.ua/', *args, **kwargs):
        super(YandexEngine, self).__init__(log_file, address, *args, **kwargs)

    def search_setup(self, query):
        self.crawler.go(self.address)
        self.crawler.choose_form(id='form')
        self.crawler.set_input('text', query)
        self.crawler.submit()

    def page_search(self):
        for a in self.crawler.css_list('.b-body-items .b-serp-item__title-link'):
            yield a.attrib.get('href', '')

    def next_page(self):
        self.page += 1
        params = self.crawler.urlencode({'text': self.query, 'tld': 'ua', 'lr': self.region, 'p': self.page})
        self.crawler.go('?'.join([self.address, params]))
