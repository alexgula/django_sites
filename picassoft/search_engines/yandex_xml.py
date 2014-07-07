# coding=utf-8
from lxml import etree
import requests
from .base import SearchEngine

QUERY_TEMPLATE = u"""<?xml version='1.0' encoding='utf-8'?>
<request>
    <query>{query}</query>
    <page>{page}</page>

    <groupings>
        <groupby groups-on-page='{results_on_page}'/>
    </groupings>
</request>"""

URL_TEMPLATE = u"http://xmlsearch.yandex.ru/xmlsearch?user={user_name}&key={key}"


class YandexXMLEngine(SearchEngine):

    verbose_name = u"Yandex (XML)"

    def __init__(self, user_name, key, results_on_page=100):
        self.url = URL_TEMPLATE.format(user_name=user_name, key=key)
        self.results_on_page = results_on_page
        self.page = 0

    def search_setup(self, query):
        self.query = query

    def page_search(self):
        post_data = QUERY_TEMPLATE.format(query=self.query, page=self.page, results_on_page=self.results_on_page)
        result = requests.post(self.url, post_data.encode('utf8'))
        root = etree.fromstring(result.content)
        for e in root.findall('*//results//group'):
            yield e.find('doc/url').text

    def next_page(self):
        self.page += 1
