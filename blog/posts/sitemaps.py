"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 17/08/21
@name: sitemaps
"""
from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    """ """
    changefreq = 'weekly'
    priority = 0.9

    def item(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
