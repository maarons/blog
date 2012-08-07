# -*- coding: utf-8 -*-

from os.path import abspath

AUTHOR = "Marek Sapota"
SITENAME = u"Marek Sapota’s blog"
SITEURL = "http://blog.marek.sapota.org"
RELATIVE_URLS = False

ARTICLE_PERMALINK_STRUCTURE = "article/%Y/%m/%d/"
DEFAULT_DATE_FORMAT = "%m/%d/%Y %H:%M"
FALLBACK_ON_FS_DATE = False
PATH = "src/"
TIMEZONE = "UTC"

FEED = "feeds/atom.xml"
CATEGORY_FEED = "feeds/category/%s/atom.xml"
TAG_FEED = "feeds/tag/%s/atom.xml"

THEME = abspath("theme/")

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = round(DEFAULT_PAGINATION / 2)
