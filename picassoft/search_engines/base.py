# coding=utf-8


class CaptchaException(Exception):
    def __unicode__(self, *args, **kwargs):
        return u"CAPTCHA detected"


class SearchResult(object):

    def __init__(self, url, page, position):
        self.url = url
        self.page = page
        self.position = position

    def contains(self, site):
        return site in self.url

    def __unicode__(self):
        return u"{}-{}) {}".format(self.page + 1, self.position + 1, self.url)


class SearchEngine(object):

    def search_urls(self, query, max_pages):
        """Do a search in the engine and return (possibly) infinite sequence of urls from the result."""
        self.search_setup(query)
        self.check_captcha()
        page = 0
        while True:
            if page >= max_pages:
                break
            for position, url in enumerate(self.page_search()):
                yield SearchResult(url, page, position)
            self.sleep()
            self.next_page()
            self.check_captcha()
            page += 1

    def search(self, query, site, max_pages=10, max_results=100):
        """Make a search in a search engine and return result for the given site."""

        for i, result in enumerate(self.search_urls(query, max_pages)):
            if i >= max_results:
                break
            if result.contains(site):
                return i, result
        return None, None

    def sleep(self):
        """Sleep some time to protect from abuse detection."""
        pass

    def search_setup(self, query):
        """Setup search for query string."""
        pass

    def page_search(self):
        """Iterate through appropriate search results.

        Each iteration returns the url of the link to a page."""
        pass

    def next_page(self):
        """Go to the next search page."""
        pass

    def check_captcha(self):
        """Check if search engine detected our bot and sent a CAPTCHA request."""
        pass
