# -*- coding: utf-8 -*-
#
# ClassicMenu Indicator - an indicator applet for Unity, that
#                         provides the main menu of Gnome2/Gnome Classic.
#
# Copyright (C) 2011 Florian Diesch <devel@florian-diesch.de>
#
# Homepage: http://www.florian-diesch.de/software/classicmenu-indicator/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import gettext
import gi
import dbus
import dbus.service
import os
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gettext import gettext as _
from optparse import OptionParser

gi.require_version('Gtk', '3.0')
gi.require_version('GMenu', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import (Gtk, GLib, GObject, GdkPixbuf, Gio, GMenu, # noqa
                           AppIndicator3)   # noqa

from . import about, preferencesdlg   # noqa
from .settings import vars as settings, FOLDERMENU   # noqa


def _add_menu_item(title, icon, callback, menu):
    menu_item = Gtk.ImageMenuItem(title)
    if icon is not None:
        menu_item.set_image(Gtk.Image.new_from_icon_name(
            icon, settings.ICON_SIZE))
    menu_item.connect('activate', callback)
    menu.append(menu_item)


def _add_stock_menu_item(stockid, callback, menu):
    menu_item = Gtk.ImageMenuItem.new_from_stock(stockid, None)
    menu_item.connect('activate', callback)
    menu.append(menu_item)

######################################################################


mainmenu = None


DBusGMainLoop(set_as_default=True)

OPATH = "/de/florian_diesch/classicmenu_indicator"
IFACE = "de.florian_diesch.classicmenu_indicator"
BUS_NAME = "de.florian_diesch.classicmenu_indicator"


class MonitorDBus(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus.request_name(BUS_NAME)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)

    @dbus.service.method(dbus_interface=IFACE,
                         in_signature="", out_signature="")
    def OpenMenu(self):
        mainmenu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

######################################################################


def _add_separator_menu_item(menu):
    menu_item = Gtk.SeparatorMenuItem()
    menu.append(menu_item)


class FolderMenuEntry:

    def __init__(self, folder, filename=None):
        self.folder = folder
        if filename is None:  # folder
            self.filename = os.path.basename(folder)
        else:
            self.filename = filename
        self.cmd = self._get_cmd()
        self.appinfo = self._create_appinfo()

    def _get_cmd(self):
        return os.path.join(self.folder, self.filename)

    def _create_appinfo(self):
        kf = GLib.KeyFile()
        try:
            kf.set_string('Desktop Entry', 'Type', 'Application')
            kf.set_string('Desktop Entry', 'Exec', self.cmd)
            kf.set_string('Desktop Entry', 'Name', self.filename)
        except Exception as e:
            raise TypeError(str(e))
        if settings.FOLDER_MENU_NEEDS_TERMINAL:
            kf.set_string('Desktop Entry', 'Terminal', 'true')
        return Gio.DesktopAppInfo.new_from_keyfile(kf)

    def get_name(self):
        return self.filename

    def get_comment(self):
        return None

    def get_icon(self):
        return None

    def get_app_info(self):
        return self.appinfo


class FolderMenuItem(FolderMenuEntry):
    pass


class FolderMenuFolder(FolderMenuEntry):
    def _get_cmd(self):
        return '/bin/sh'

    def get_icon(self):
        return Gio.ThemedIcon.new('applications-other')


class ClassicMenuIndicator(object):
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            settings.app_name,
            settings.ICON,
            settings.category)

        gettext.bindtextdomain(settings.GETTEXT_DOMAIN)
        gettext.textdomain(settings.GETTEXT_DOMAIN)
        gettext.bind_textdomain_codeset(settings.GETTEXT_DOMAIN, 'UTF-8')

        self.theme = Gtk.IconTheme.get_default()

        self.update_requested = False
        self.entries = set()  # for removing duplicates

        self.indicator.set_status(
            AppIndicator3.IndicatorStatus.ACTIVE)

        self.create_all_trees()
        self.menu = self.create_menu()

        global mainmenu
        mainmenu = self.menu

        self.indicator.set_menu(self.menu)

    def run(self):
        MonitorDBus()
        try:
            Gtk.main()
        except KeyboardInterrupt:
            pass

    def add_folder_menu(self, menu):
        root = settings.FOLDER_MENU_ROOT
        files = sorted((r, f) for r, ds, fs in os.walk(root) for f in fs + ds)
        submenus = {}

        for adir, afile in files:
            cmd = os.path.join(adir, afile)
            if adir not in submenus:
                try:
                    entry = FolderMenuFolder(adir)
                except TypeError as e:
                    print(e)
                new_menu, menu_item = self.create_sub_menu_for_entry(entry)
                submenus[adir] = new_menu
                if adir == root:
                    menu.append(menu_item)
                else:
                    parent = os.path.dirname(adir)

                    # insert after last menu in parent:
                    children = submenus[parent].get_children()
                    i = 0
                    for i, child in enumerate(children):
                        if child.get_submenu() is None:
                            break
                    submenus[parent].insert(menu_item, i)
            if not (
                afile.endswith('~') or
                afile.endswith('#') or
                afile.startswith('.') or
                not os.access(cmd, os.X_OK)
            ):

                try:
                    entry = FolderMenuItem(adir, afile)
                except TypeError:  # can't create Gio.DesktopAppInfo
                    continue
                submenus[adir].append(self.create_menu_item(entry))

    def create_sub_menu_for_entry(self, entry):
        new_menu = Gtk.Menu()
        menu_item = self.create_menu_item(entry)
        menu_item.set_submenu(new_menu)
        menu_item.show()
        return new_menu, menu_item

    def create_menu_item(self, entry):
        try:
            name = entry.get_app_info().get_name()
        except AttributeError:
            name = entry.get_name()
        try:
            comment = entry.get_app_info().get_description()
        except AttributeError:
            comment = entry.get_comment()

        menu_item = Gtk.ImageMenuItem(name)

        img = None

        if settings.USE_MENU_ICONS:
            try:
                icon = entry.get_icon()
            except AttributeError:
                icon = entry.get_app_info().get_icon()

            if icon and not self.theme.lookup_by_gicon(
                    icon, settings.ICON_SIZE,
                    Gtk.IconLookupFlags.USE_BUILTIN):
                icon = None

            if hasattr(icon, 'get_file'):
                gfile = icon.get_file()
                if not gfile.query_exists(None):
                    icon = None
            if icon:
                    img = Gtk.Image.new_from_gicon(
                        icon, settings.ICON_SIZE)
            else:
                icon_info = self.theme.choose_icon(
                    ['gtk-execute', 'application-x-executable',
                     'applications-other'],
                    settings.ICON_SIZE,
                    Gtk.IconLookupFlags.USE_BUILTIN)
                if icon_info is not None:
                    pixbuf = icon_info.load_icon()
                    pixbuf.scale_simple(
                        16,
                        16,
                        GdkPixbuf.InterpType.BILINEAR)
                    img = Gtk.Image.new_from_pixbuf(pixbuf)

            if img is None:
                img = Gtk.Image()
                img.set_from_icon_name(
                    'application-x-executable',
                    settings.ICON_SIZE)
            menu_item.set_image(img)

            menu_item.set_always_show_image(True)

        menu_item.set_label(name)

        if isinstance(entry, (GMenu.TreeEntry, FolderMenuItem)):
            menu_item.connect('activate', self.on_menuitem_activate, entry)

        menu_item.set_use_underline(False)
        if comment is not None:
            menu_item.set_tooltip_text(comment)

        menu_item.show()
        return menu_item

    def process_entry(self, menu, entry):
        try:
            appinfo = entry.get_app_info()
            cmd = appinfo.get_commandline()
        except AttributeError:  # Can this happen?
            cmd = None

        if (
            settings.REMOVE_DUPLICATES and
            cmd is not None and
            cmd in self.entries
           ):
            return
        else:
            self.entries.add(cmd)
        menu.append(self.create_menu_item(entry))

    def process_directory(self, menu, dir):
        if dir:
            diter = dir.iter()
            type = diter.next()
            while type != GMenu.TreeItemType.INVALID:
                if type == GMenu.TreeItemType.ENTRY:
                    self.process_entry(menu, diter.get_entry())
                elif type == GMenu.TreeItemType.DIRECTORY:
                    new_menu = Gtk.Menu()
                    item = diter.get_directory()
                    menu_item = self.create_menu_item(item)
                    menu_item.set_submenu(new_menu)
                    menu.append(menu_item)
                    menu_item.show()
                    self.process_directory(new_menu, item)
                elif type == GMenu.TreeItemType.ALIAS:
                    item = diter.get_aliase()
                    # FIXME: other types
                    aliased = item.get_aliased_entry()
                    if aliased.get_type() == GMenu.TreeItemType.ENTRY:
                        self.process_entry(menu, aliased)
                elif type == GMenu.TreeItemType.SEPARATOR:
                    menu_item = Gtk.SeparatorMenuItem()
                    menu.append(menu_item)
                    menu_item.show()
                elif type in [GMenu.TreeItemType.HEADER]:
                    pass
                else:
                    print('Unsupported item type: %s' % type)
                type = diter.next()

    def add_to_menu(self, menu, tree):
        self.entries = set()
        root = tree.get_root_directory()
        self.process_directory(menu, root)

    def create_menu(self):
        menu = Gtk.Menu()

        for t in self.trees:
            if t == FOLDERMENU:
                self.add_folder_menu(menu)
            elif t:
                self.add_to_menu(menu, t)
                menu_item = Gtk.SeparatorMenuItem()
                menu.append(menu_item)

        menu_item = Gtk.MenuItem('%s' % settings.APP_NAME)
        menu.append(menu_item)

        submenu = Gtk.Menu()
        menu_item.set_submenu(submenu)

        _add_stock_menu_item(
            Gtk.STOCK_PREFERENCES,
            self.on_menuitem_preferences_activate,
            submenu)

        _add_menu_item(
            _('Reload menu'),
            'gtk-refresh',
            self.on_menuitem_reload_activate,
            submenu)

        _add_separator_menu_item(submenu)

        _add_stock_menu_item(
            Gtk.STOCK_ABOUT,
            self.on_menuitem_about_activate,
            submenu)

        _add_menu_item(_('Go to Web Page'),
                       settings.WEB_PAGE_ICON,
                       self.on_menuitem_goto_webpage,
                       submenu)

        _add_separator_menu_item(submenu)

        _add_menu_item(
            _('Report a bug in %s') % settings.APP_NAME,
            settings.WEB_PAGE_ICON,
            self.on_menuitem_bug,
            submenu)

        _add_menu_item(
            _('Help with Translations'),
            settings.WEB_PAGE_ICON,
            self.on_menuitem_translations,
            submenu)

        _add_menu_item(
            _('Donate via PayPal'),
            settings.WEB_PAGE_ICON,
            self.on_menuitem_donate,
            submenu)

        _add_separator_menu_item(submenu)

        _add_menu_item(
            _('Quit %s') % settings.APP_NAME,
            Gtk.STOCK_QUIT,
            self.on_menuitem_quit_activate,
            submenu)

        menu.show_all()
        return menu

    def create_all_trees(self):
        self.trees = []

        if settings.USE_ALL_APPS_MENU:
            tree = self.create_tree(settings.ALL_APPS_MENU)
            if tree:
                self.trees.append(tree)
        for m in settings.MENUS:
            if m == FOLDERMENU:
                tree = FOLDERMENU
            else:
                tree = self.create_tree(m)
            if tree:
                self.trees.append(tree)
        if settings.USE_EXTRA_MENUS:
            tree = self.create_tree(settings.EXTRA_MENU)
            if tree:
                self.trees.append(tree)

    def create_tree(self, name):
        flags = (GMenu.TreeFlags.SHOW_ALL_SEPARATORS |
                 GMenu.TreeFlags.SORT_DISPLAY_NAME)

        if settings.INCLUDE_NODISPLAY:
            flags = flags | GMenu.TreeFlags.INCLUDE_NODISPLAY

        try:
            if '/' in name:
                tree = GMenu.Tree.new_for_path(name, flags)
            else:
                tree = GMenu.Tree.new(name, flags)
            tree.load_sync()
            tree.connect('changed', self.on_menu_file_changed)
            return tree
        # except GLib.Error as e:
        except Exception as e:
            print(type(e))
            print('***', e)

    def update_menu(self, recreate_trees=False):
        self.update_requested = False
        if recreate_trees:
            self.create_all_trees()

        new_menu = self.create_menu()
        global mainmenu
        mainmenu = new_menu

        self.indicator.set_menu(new_menu)
        return False    # Don't run again

    def request_update(self, recreate_trees=False, delayed=True):
        if not self.update_requested:
            self.update_requested = True
            if delayed:
                GObject.timeout_add(settings.UPDATE_DELAY,
                                    lambda: self.update_menu(recreate_trees))
            else:
                self.update_menu(recreate_trees)

    def quit(self):
        Gtk.main_quit()

    def open_url(self, url):
        Gio.AppInfo.launch_default_for_uri(url, None)

    def reload(self, delayed=True):
        settings.load()
        self.indicator.set_icon(settings.ICON)
        self.request_update(recreate_trees=True, delayed=delayed)

    def show_reload_msg(self):
        dlg = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                Gtk.ButtonsType.NONE,
                                _('Updating menu...'))
        dlg.set_title(_('Please wait'))
        GLib.timeout_add(500, lambda *args: dlg.destroy())
        dlg.run()

    def on_menu_file_changed(self, *args):
        self.reload()

    def on_menuitem_activate(self, menuitem, entry):
        appinfo = entry.get_app_info()
        if appinfo is not None:
            appinfo.launch([], None)

    def on_menuitem_preferences_activate(self, menuitem):
        dlg = preferencesdlg.PreferencesDlg()
        if dlg.run():
            self.show_reload_msg()
            self.reload(delayed=False)

    def on_menuitem_quit_activate(self, menuitem):
        self.quit()

    def on_menuitem_reload_activate(self, menuitem):
        self.show_reload_msg()
        self.reload(delayed=False)

    def on_menuitem_about_activate(self, menuitem):
        about.show_about_dialog()

    def on_menuitem_docs(self, menuitem):
        self.open_url(settings.LOCAL_DOCS_URL)

    def on_menuitem_goto_webpage(self, menuitem):
        self.open_url(settings.WEB_URL)

    def on_menuitem_donate(self, menuitem):
        self.open_url(settings.PAYPAL_URL)

    def on_menuitem_translations(self, menuitem):
        self.open_url(settings.TRANSLATIONS_URL)

    def on_menuitem_bug(self, menuitem):
        self.open_url(settings.BUGREPORT_URL)


def parse_args():
    parser = OptionParser(version="%s %s" % (settings.APP_NAME,
                                             settings.APP_VERSION))

    help = _('Show menu at mouse pointer location. This requires an '
             'already running instance of %s' % settings.APP_NAME)
    parser.add_option('-m', '--show-menu', action="store_true",
                      dest='show_menu', default=False,
                      help=help)

    help = _('Start a new instance of %s, even if there alread is one'
             'running' % settings.APP_NAME)
    parser.add_option('-i', '--ignore-running', action="store_true",
                      dest='ignore', default=False,
                      help=help)

    options, args = parser.parse_args()
    return options, args


def main():
    options, args = parse_args()
    if options.show_menu:
        try:
            api = dbus.Interface(
                dbus.SessionBus().get_object(IFACE, OPATH), BUS_NAME)
            api.OpenMenu()
        except Exception as e:
            print(_("Can't connect to %s:\n%s\n") % (
                settings.APP_NAME, e))
            print(_("Maybe you need to start %s first.") % settings.APP_NAME)
            sys.exit(1)
    else:
        if not options.ignore:
            try:  # CMI alread running?
                api = dbus.Interface(dbus.SessionBus().get_object(
                    IFACE, OPATH), BUS_NAME)
                print(_('%s already running. Not starting another one.\n'
                        'Use the "--ignore-running" option if you want to '
                        'start more than one instance.'
                        % settings.APP_NAME))
                sys.exit(2)
            except Exception as e:
                pass

        indicator = ClassicMenuIndicator()
        indicator.run()
