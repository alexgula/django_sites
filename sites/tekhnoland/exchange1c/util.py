# coding=utf-8
"""Utility functions for manual testing of the exchange."""
import requests
from picassoft.utils.http import get_basic_auth_header


def auth(domain, qtype, user, password):
    auth_header = get_basic_auth_header(user, password)
    url = "http://{}/catalog/exchange/?type={}&mode=checkauth".format(domain, qtype)
    r = requests.get(url, headers={'Authorization': auth_header})
    return r.content


def sale(domain, mode, exchangeid, filepath):
    url = "http://{}/catalog/exchange/?type=sale&mode={}".format(domain, mode)
    cookies = {'exchangeid': exchangeid}
    with open(filepath, 'w') as f:
        r = requests.get(url, cookies=cookies)
        f.write(r.content)


def catalog(domain, mode, exchangeid, filepath):
    url = "http://{}/catalog/exchange/?type=catalog&mode={}".format(domain, mode)
    cookies = {'exchangeid': exchangeid}
    with open(filepath, 'w') as f:
        r = requests.get(url, cookies=cookies)
        f.write(r.content)


if __name__ == "__main__":
    # Usage example
    auth('192.168.1.11:8002', 'catalog')
    catalog('192.168.1.11:8002', 'import', '4c69fbf1cb76be3525dea05519ef3e56', 'E:/import.xml')
    sale('192.168.1.11:8002', 'query', '4c69fbf1cb76be3525dea05519ef3e56', 'E:/sale.xml')
