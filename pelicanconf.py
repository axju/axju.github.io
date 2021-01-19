#!/usr/bin/env python
# -*- coding: utf-8 -*- #

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

DEFAULT_PAGINATION = 10

EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'},
}

DISPLAY_PAGES_ON_MENU = True

GITHUB_URL = 'https://github.com/axju'

# Theme settings

THEME = 'themes/alchemy'
THEME_CSS_OVERRIDES = ['theme/css/oldstyle.css']

SITESUBTITLE = 'Just coding stuff'

SITEIMAGE = 'images/logo.png'

HIDE_AUTHORS = True
RFG_FAVICONS = False
