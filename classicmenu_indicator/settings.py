#-*- coding: utf-8 -*-

import os, os.path
import appindicator
import xdg.BaseDirectory

import config
import _version


APP_NAME = 'ClassicMenu Indicator'
APP_VERSION  = _version.VERSION
app_name = 'classicmenu-indicator'


USER_CONFIG_HOME = xdg.BaseDirectory.xdg_config_home

APP_CONFIG_HOME = os.path.join(USER_CONFIG_HOME, app_name)

CFG_FILE =  os.path.join(APP_CONFIG_HOME, 'config')

cfg = config.Config(CFG_FILE)

WEB_URL = 'http://www.florian-diesch.de/software/%s/' % app_name

if os.path.isfile('.is-devel-dir'):
    DATA_DIR = 'data'
else: 
    DATA_DIR = '/usr/share/classicmenu-indicator'

UI_DIR = os.path.join(DATA_DIR, 'ui')

ICON = cfg.get('icon', 'distributor-logo')
ICON_SIZE = cfg.get('icon_size', 22, int)

INCLUDE_NODISPLAY=cfg.get('include_nodisplay', False)

SYSTEM_MENUS = ['settings.menu',  
                'classicmenuindicatorsystem.menu']

EXTRA_MENUS = []

category = appindicator.CATEGORY_SYSTEM_SERVICES

GETTEXT_DOMAIN='classicmenu-indicator'

LOCAL_DOCS_URL = 'man:X'
PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DJCGEPS4746PU'
FLATTR_URL = 'http://flattr.com/thing/420221/ClassicMenu-Indicator'

TRANSLATIONS_URL = 'https://translations.launchpad.net/classicmenu-indicator'

BUGREPORT_URL = 'https://bugs.launchpad.net/classicmenu-indicator/+filebug'
