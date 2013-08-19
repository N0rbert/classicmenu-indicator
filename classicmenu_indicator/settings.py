#-*- coding: utf-8 -*-

import os, os.path
import appindicator
import xdg.BaseDirectory

import config
import _meta


APP_NAME = _meta.TITLE
APP_VERSION  = _meta.VERSION
app_name = _meta.NAME

WEB_URL = _meta.WEB_URL

AUTHOR_EMAIL = _meta.AUTHOR_EMAIL
AUTHOR_NAME = _meta.AUTHOR_NAME

USER_CONFIG_HOME = xdg.BaseDirectory.xdg_config_home

APP_CONFIG_HOME = os.path.join(USER_CONFIG_HOME, app_name)

CFG_FILE =  os.path.join(APP_CONFIG_HOME, 'config')

cfg = config.Config(CFG_FILE)


if os.path.isfile('.is-devel-dir'):
    DATA_DIR = 'data'
else: 
    DATA_DIR = '/usr/share/classicmenu-indicator'

UI_DIR = os.path.join(DATA_DIR, 'ui')

ICON = cfg.get('my_icon', 'classicmenu-indicator')
ICON_SIZE = cfg.get('icon_size', 22, int)

USE_MENU_ICONS = cfg.get('menu_icons', True)

INCLUDE_NODISPLAY=cfg.get('include_nodisplay', False)

SYSTEM_MENUS = ['settings.menu',  
                'classicmenuindicatorsystem.menu']

EXTRA_MENUS = []

category = appindicator.CATEGORY_SYSTEM_SERVICES

GETTEXT_DOMAIN = app_name

LOCAL_DOCS_URL = None
PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DJCGEPS4746PU'
FLATTR_URL = 'http://flattr.com/thing/420221/ClassicMenu-Indicator'

TRANSLATIONS_URL = 'https://translations.launchpad.net/classicmenu-indicator'

BUGREPORT_URL = 'https://bugs.launchpad.net/classicmenu-indicator/+filebug'
