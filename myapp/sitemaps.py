from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Item

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['sign-in', 'sign-up', 'home']

    def location(self, item):
        return reverse(item)

class Item_Sitemap(Sitemap):
    changefreq = "never"
    priority = 0.7

    def items(self):
        return Item.objects.all()

    def location(self, obj):
        return reverse('post', kwargs={'id':obj.id})

    def lastmod(self, obj): 
        return obj.date_crawled