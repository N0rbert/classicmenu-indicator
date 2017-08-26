#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import classicmenu_indicator
import classicmenu_indicator.settings
import os.path
import sys

fullpath = os.path.abspath(__file__)
path = os.path.split(fullpath)[0]
sys.path = [path] + sys.path

DATA_DIR = os.path.normpath(os.path.join(path, 'data'))

classicmenu_indicator.settings.Vars.DATA_DIR = DATA_DIR
classicmenu_indicator.settings.Vars.UI_DIR = os.path.join(DATA_DIR, 'ui')
classicmenu_indicator.settings.Vars.ICON_DIR = os.path.join(DATA_DIR, 'icons')
classicmenu_indicator.settings.Vars.EXTRA_MENU = os.path.join(DATA_DIR, 'menu', 'applications.menu')
classicmenu_indicator.settings.Vars.ALL_APPS_MENU = os.path.join(DATA_DIR, 'menu', 'all_apps.menu')

classicmenu_indicator.main()
