# -*- coding: utf-8 -*-

from os.path import abspath

AUTHOR = "Marek Sapota"
SITENAME = u"Marek Sapota’s blog"
SITEURL = "http://blog.marek.sapota.org"
RELATIVE_URLS = False

ARTICLE_URL = "article/{date:%Y}/{date:%m}/{date:%d}/{slug}.html"
ARTICLE_SAVE_AS = ARTICLE_URL
DEFAULT_DATE_FORMAT = "%m/%d/%Y %H:%M"
DEFAULT_DATE = None
PATH = "src/"
TIMEZONE = "UTC"

FEED_DOMAIN = SITEURL
FEED_ATOM = "feeds/atom.xml"
FEED_RSS = "feeds/rss.xml"
CATEGORY_FEED_ATOM = "feeds/category/%s/atom.xml"
CATEGORY_FEED_RSS = "feeds/category/%s/rss.xml"
TAG_FEED_ATOM = "feeds/tag/%s/atom.xml"
TAG_FEED_RSS = "feeds/tag/%s/rss.xml"
FEED_MAX_ITEMS = 10

THEME = abspath("theme/")

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = round(DEFAULT_PAGINATION / 2)
