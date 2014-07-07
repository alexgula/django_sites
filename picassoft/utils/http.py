# coding=utf-8
import base64
import requests


def redirs(url):
    """List redirects of the given url.

    Returns final response and history of redirect urls leading to it."""
    result = requests.get(url)
    return result, [(h.status_code, h.headers['location']) for h in result.history]


def get_basic_auth_header(login, password):
    return 'Basic ' + base64.standard_b64encode('{}:{}'.format(login, password))


def post_xml(url, data, login, password, use_post_method=True):
    auth = get_basic_auth_header(login, password)
    method = requests.post if use_post_method else requests.get
    return method(url, data, headers={'Authorization': auth, 'Content-type': 'text/xml;encoding=utf-8'})


def post_xml_file(url, file_path, login, password):
    with open(file_path, 'rb') as f:
        data = f.read()
        return post_xml(url, data, login, password)
