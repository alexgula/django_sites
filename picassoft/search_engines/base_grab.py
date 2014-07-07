# coding=utf-8
import os
from grab import Grab
from .base import CaptchaException, SearchEngine


class GrabEngine(SearchEngine):
    def __init__(self, log_file, address, log_dir='', debug=False, language='ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
                 charset='utf-8', sleep_max=4):
        log_path = os.path.join(log_dir, log_file) if log_dir else log_file
        self.crawler = Grab(log_file=log_path)
        self.crawler.setup(debug=debug)  # Option `debug` enables saving of outgoing requests headers
        self.crawler.setup(headers={'Accept-Language': language, 'Accept-Charset': charset})
        #self.crawler.setup(proxy='113.122.35.15:8909', proxy_type='http', connect_timeout=25, timeout=25)
        self.sleep_max = sleep_max if sleep_max > 1 else 1
        self.address = address

    def sleep(self):
        self.crawler.sleep(limit2=self.sleep_max)

    def check_captcha(self):
        if self.crawler.xpath_list(self.captcha_selector):
            raise CaptchaException()
