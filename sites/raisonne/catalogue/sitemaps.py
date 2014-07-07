from .models import Author, Work
from picassoft.utils.sitemaps import MultiLocaleSitemap

class AuthorSitemap(MultiLocaleSitemap):
    def _items(self):
        return Author.objects.all()

class WorkSitemap(MultiLocaleSitemap):
    def _items(self):
        return Work.objects.all()
