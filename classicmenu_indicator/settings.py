#-*- coding: utf-8 -*-

import os, os.path
import appindicator

import config
import _version


APP_NAME = 'ClassicMenu Indicator'
APP_VERSION  = _version.VERSION
app_name = 'classicmenu-indicator'



cfg = config.Config(os.path.expanduser('~/.config/%s/config' % app_name))

WEB_URL = 'http://www.florian-diesch.de/software/classicmenu-indicator/'

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

PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DJCGEPS4746PU'
FLATTR_URL = 'http://flattr.com/thing/420221/ClassicMenu-Indicator'

TRANSLATIONS_URL = 'https://translations.launchpad.net/classicmenu-indicator'

BUGREPORT_URL = 'https://bugs.launchpad.net/classicmenu-indicator/+filebug'
