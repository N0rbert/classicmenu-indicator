import os, os.path
import appindicator

APP_NAME = 'ClassicMenu Indicator'
APP_VERSION  = '0.07'
app_name = 'classicmenu-indicator'


WEB_URL = 'http://www.florian-diesch.de/software/classicmenu-indicator/'

if os.path.isfile('.is-devel-dir'):
    DATA_DIR = 'data'
else: 
    DATA_DIR = '/usr/share/classicmenu-indicator'

UI_DIR = os.path.join(DATA_DIR, 'ui')

ICON = 'start-here'
category = appindicator.CATEGORY_SYSTEM_SERVICES

GETTEXT_DOMAIN='classcimenu-indicator'

PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DJCGEPS4746PU'
