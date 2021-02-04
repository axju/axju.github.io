#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from datetime import datetime

AUTHOR = 'Axel Juraske'
SITENAME = 'axju'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
ICONS = (('github', 'https://github.com/axju'),
         ('youtube', 'https://www.youtube.com/channel/UCFFrfCiHAh0gaQvGZBYMsuA'),
         ('twitter', 'https://twitter.com/0xAxJu'),)

FOOTER_ICONS = (('rss', 'feeds/all.atom.xml'),)

DEFAULT_PAGINATION = 10

EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'},
}

DISPLAY_PAGES_ON_MENU = True

GITHUB_URL = 'https://github.com/axju'

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['fontawesome', 'shields']
# PLUGINS = [
#     'pelican_fontawesome',
# ]
# CSS_FILE = 'oldstyle.css'

STATIC_PATHS = ['images', ]
ARTICLE_PATHS = ['articles']

# Theme settings

THEME = 'themes/axju'

DATE = datetime.now()

SITESUBTITLE = 'Just coding stuff'

SITEIMAGE = 'images/logo.png'

PYGMENTS_STYLE = 'native'

HIDE_AUTHORS = True
RFG_FAVICONS = False
