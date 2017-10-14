# -*- coding: utf-8 -*-

import glob
import json
import os
import os.path
from gi.repository import Gtk, AppIndicator3
from gettext import gettext as _
from . import _meta

_config_home = os.path.expanduser(os.path.join('~', '.config'))
config_home = os.environ.get('XDG_CONFIG_HOME', _config_home)

FOLDERMENU = _('*Simple Menu*')


def get_all_menu_files():
    dirs = os.environ.get('XDG_CONFIG_DIRS', '/etc/xdg')
    result = set([FOLDERMENU])
    for d in dirs.split(':') + [config_home]:
        for m in glob.glob(os.path.join(d, 'menus', '*.menu')):
            result.add(os.path.basename(m))
    return sorted(result)


def get_default_menu_files():
    no_prefix_menus = {
        'MATE': 'mate-',
        'kde-plasma': 'kde4-',
        'cinnamon': 'cinnamon-',
    }

    menu_prefix = os.getenv('XDG_MENU_PREFIX', '')
    desktop = os.getenv('XDG_CURRENT_DESKTOP', '')

    if menu_prefix == '' and desktop in no_prefix_menus:
        menu_prefix = no_prefix_menus[desktop]

    menu = '{prefix}applications.menu'.format(prefix=menu_prefix)

    all_menus = set(get_all_menu_files())

    result = [FOLDERMENU]

    fallback_menus = (
        '{desktop}-applications.menu'.format(desktop=desktop),
        'applications.menu',
        'gnome-applications.menu'
    )

    if menu in all_menus:
        result.append(menu)
    else:
        for fm in fallback_menus:
            if fm in all_menus:
                result.append(fm)
                break

    return [m for m in result if m in all_menus]


class Vars(object):

    APP_NAME = _meta.TITLE
    APP_VERSION = _meta.VERSION
    app_name = _meta.NAME

    WEB_URL = _meta.WEB_URL

    AUTHOR_EMAIL = _meta.AUTHOR_EMAIL
    AUTHOR_NAME = _meta.AUTHOR_NAME

    USER_CONFIG_HOME = config_home
    APP_CONFIG_HOME = os.path.join(USER_CONFIG_HOME, app_name)
    CFG_FILE = os.path.join(APP_CONFIG_HOME, 'config.json')

    def __init__(self):
        try:
            os.makedirs(self.APP_CONFIG_HOME)
        except OSError as e:
            if e.errno != 17:  # dir exists
                print(e)

        self.load()

    def set_to_defaults(self):
        self.data = {}

    def load(self):
        try:
            with open(self.CFG_FILE) as input:
                self.data = json.load(input)
        except Exception as e:
            self.set_to_defaults()

    def save(self):
        with open(self.CFG_FILE, 'w') as cfg:
            json.dump(self.data, cfg, sort_keys=True, indent=4)

    ICONS = {'old': 'start-here',
             'dark': 'classicmenu-indicator-light',  # for light theme
             'light': 'classicmenu-indicator-dark',  # for dark theme
             'auto': 'classicmenu-indicator',
             }

    WEB_PAGE_ICON = 'go-jump'

    DATA_DIR = '/usr/share/classicmenu-indicator'

    UI_DIR = os.path.join(DATA_DIR, 'ui')

    EXTRA_MENU = os.path.join(DATA_DIR, 'applications.menu')
    ALL_APPS_MENU = os.path.join(DATA_DIR, 'all_apps.menu')

    @property
    def ICON(self):
        return self.data.get('my_icon', self.ICONS['auto'])

    @ICON.setter
    def ICON(self, value):
        self.data['my_icon'] = value

    @property
    def ICON_SIZE(self):
        return self.data.get('icon_size', Gtk.IconSize.MENU)

    @ICON_SIZE.setter
    def ICON_SIZE(self, value):
        self.data['icon_size'] = value

    @property
    def USE_MENU_ICONS(self):
        return self.data.get('menu_icons', False)

    @USE_MENU_ICONS.setter
    def USE_MENU_ICONS(self, value):
        self.data['menu_icons'] = value

    @property
    def UPDATE_DELAY(self):
        return self.data.get('update_delay', 5000)

    @UPDATE_DELAY.setter
    def UPDATE_DELAY(self, value):
        self.data['update_delay'] = value

    @property
    def INCLUDE_NODISPLAY(self):
        return self.data.get('include_nodisplay', False)

    @INCLUDE_NODISPLAY.setter
    def INCLUDE_NODISPLAY(self, value):
        self.data['include_nodisplay'] = value

    @property
    def REMOVE_DUPLICATES(self):
        return self.data.get('remove_duplicates', False)

    @REMOVE_DUPLICATES.setter
    def REMOVE_DUPLICATES(self, value):
        self.data['remove_duplicates'] = value

    @property
    def MENUS(self):
        return self.data.get('menus', get_default_menu_files())

    @MENUS.setter
    def MENUS(self, value):
        self.data['menus'] = value

    @property
    def USE_TOOLTIPS(self):
        return self.data.get('use_tooltips', False)

    @USE_TOOLTIPS.setter
    def USE_TOOLTIPS(self, value):
        self.data['use_tooltips'] = value

    @property
    def USE_EXTRA_MENUS(self):
        return self.data.get('use_extra_menus', True)

    @USE_EXTRA_MENUS.setter
    def USE_EXTRA_MENUS(self, value):
        self.data['use_extra_menus'] = value

    @property
    def USE_ALL_APPS_MENU(self):
        return self.data.get('use_all_apps_menu', False)

    @USE_ALL_APPS_MENU.setter
    def USE_ALL_APPS_MENU(self, value):
        self.data['use_all_apps_menu'] = value

    @property
    def FOLDER_MENU_NEEDS_TERMINAL(self):
        return self.data.get('folder_menu_needs_terminal', True)

    @FOLDER_MENU_NEEDS_TERMINAL.setter
    def FOLDER_MENU_NEEDS_TERMINAL(self, value):
        self.data['folder_menu_needs_terminal'] = value

    @property
    def FOLDER_MENU_ROOT(self):
        return self.data.get('folder_menu_root', os.path.expanduser(
            os.path.join('~', 'bin')))

    @FOLDER_MENU_ROOT.setter
    def FOLDER_MENU_ROOT(self, value):
        self.data['folder_menu_root'] = value

    category = AppIndicator3.IndicatorCategory.SYSTEM_SERVICES

    GETTEXT_DOMAIN = app_name

    LOCAL_DOCS_URL = None
    PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DJCGEPS4746PU'  # noqa

    TRANSLATIONS_URL = 'https://translations.launchpad.net/classicmenu-indicator'  # noqa

    BUGREPORT_URL = 'https://bugs.launchpad.net/classicmenu-indicator/+filebug'


vars = Vars()
