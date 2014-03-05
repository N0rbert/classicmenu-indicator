#!/usr/bin/env python
#-*- coding: utf-8 -*-
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


import gmenu
import gtk, glib, gobject, gio, gtk.gdk
import appindicator
import re, os
import textwrap
import subprocess
from optparse import OptionParser
from urlparse import urlparse
import pynotify

import about

from settings import vars as settings

from gettext import gettext as _
import gettext
import xdg.IconTheme as xdgicon


class ClassicMenuIndicator(object):
    def __init__(self):
        self.indicator = appindicator.Indicator(settings.app_name,
                                                settings.ICON,
                                                settings.category)

        gettext.bindtextdomain(settings.GETTEXT_DOMAIN)
        gettext.textdomain(settings.GETTEXT_DOMAIN)
        gettext.bind_textdomain_codeset(settings.GETTEXT_DOMAIN, 'UTF-8')

        self.have_notify = True
        if not pynotify.init(settings.APP_NAME):
            self.have_notify = False

        screen = gtk.gdk.screen_get_default()
        self.theme = gtk.icon_theme_get_for_screen(screen)

        self.update_requested = False

        self.indicator.set_status (appindicator.STATUS_ACTIVE)

        self.create_all_trees()
        
        self.indicator.set_menu(self.create_menu())

        settings.cfg.set_callback(self.on_config_changed)
        
    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass


    def notify(self, msg, type='Information'):
        print 'NOTIFY:',  self.have_notify, settings.USE_NOTIFY
        if self.have_notify and settings.USE_NOTIFY:
            n = pynotify.Notification(type, msg)
            if not n.show():
                print "Failed to send notification"
            

    def create_menu_item(self, entry):
        name = entry.get_name()
        comment = entry.get_comment() 

        menu_item = gtk.ImageMenuItem(name)
        
        icon = entry.get_icon()
 
        img = None
        if icon:
            try:
                if self.theme.lookup_icon(icon, settings.ICON_SIZE, 
                                          gtk.ICON_LOOKUP_USE_BUILTIN):
                    pixbuf = self.theme.load_icon(icon, settings.ICON_SIZE, 
                                                  gtk.ICON_LOOKUP_USE_BUILTIN)
                    if pixbuf.get_height() > settings.ICON_SIZE:
                        scale = pixbuf.get_height() / float(settings.ICON_SIZE)
                        width = int(pixbuf.get_width() * scale)
                        pixbuf.scale_simple(width, settings.ICON_SIZE, 
                                            gtk.gdk.INTERP_BILINEAR)
                    img = gtk.image_new_from_pixbuf(pixbuf)
                else:
                    icon_path = xdgicon.getIconPath(icon)
                    if icon_path:
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                            icon_path, 
                            settings.ICON_SIZE,
                            settings.ICON_SIZE)
                        img = gtk.image_new_from_pixbuf(pixbuf)
                    # else:
                    #     img = gtk.Image()
                    #     print 'FROM NAME'
                    #     img.set_from_icon_name(icon, settings.ICON_SIZE)

            except glib.GError, e:
                print '[%s] "%s": %s: %s'%(settings.APP_NAME, name, icon , e)

                
        if settings.USE_MENU_ICONS:
            if img is None:
                img = gtk.Image()
                img.set_from_icon_name('gtk-execute', settings.ICON_SIZE)

            menu_item.set_image(img)
            menu_item.set_label(name)
            menu_item.set_always_show_image(True)
           
        if entry.get_type() ==  gmenu.TYPE_ENTRY:
            menu_item.connect('activate', self.on_menuitem_activate, entry)

        menu_item.set_use_underline(False)
        menu_item.set_tooltip_text(comment)

        menu_item.show()
        return menu_item



    def process_entry(self, menu, entry):
        menu.append(self.create_menu_item(entry))

    
    def process_directory(self, menu, dir):
        if dir:
            for item in dir.get_contents():
                type = item.get_type()
                if type == gmenu.TYPE_ENTRY:
                    self.process_entry(menu, item)
                elif type == gmenu.TYPE_DIRECTORY:
                    new_menu = gtk.Menu()
                    menu_item = self.create_menu_item(item)
                    menu_item.set_submenu(new_menu)
                    menu.append(menu_item)
                    menu_item.show()
                    self.process_directory(new_menu, item)
                elif type == gmenu.TYPE_ALIAS:
                    aliased = item.get_item()
                    if aliased.get_type() == gmenu.TYPE_ENTRY:
                        self.process_entry(menu, aliased)
                elif type == gmenu.TYPE_SEPARATOR:
                    menu_item = gtk.SeparatorMenuItem()
                    menu.append(menu_item)
                    menu_item.show()
                elif type in [ gmenu.TYPE_HEADER ]:
                    pass
                else:
                    print >> sys.stderr, 'Unsupported item type: %s' % type


    def add_to_menu(self, menu, tree):
        root = tree.get_root_directory()    
        self.process_directory(menu, root)

    def add_config_menu_items(self, menu):
        
        menu_item = gtk.CheckMenuItem(_('Use old icon'))
        menu_item.set_active(settings.ICON == settings.OLD_ICON)
        def callback(item, *args):
            settings.set_use_old_icon(item.get_active())            
        menu_item.connect('toggled', callback)        
        menu.append(menu_item)

        menu_item = gtk.CheckMenuItem(_('Show menu icons'))
        menu_item.set_active(settings.USE_MENU_ICONS)
        def callback(item, *args):
            settings.set_use_menu_icons(item.get_active())
        menu_item.connect('toggled', callback)        
        menu.append(menu_item)
        
        menu_item = gtk.CheckMenuItem(_('Show notifications'))
        menu_item.set_active(settings.USE_NOTIFY)
        def callback(item, *args):
            settings.set_use_notify(item.get_active())
        menu_item.connect('toggled', callback)
        menu.append(menu_item)

        if self.is_unity():
            menu_item = gtk.CheckMenuItem(_('Use alternate menu'))
            menu_item.set_active(settings.USE_LENS_MENU)
            def callback(item, *args):
                settings.set_use_lens_menu(item.get_active())
            menu_item.connect('toggled', callback)        
            menu.append(menu_item) 
        
    def create_menu(self):
        menu = gtk.Menu()

        for t in self.trees:
            if t:
                self.add_to_menu(menu, t)
                menu_item = gtk.SeparatorMenuItem()
                menu.append(menu_item)

        menu_item = gtk.MenuItem('%s' % settings.APP_NAME)
        menu.append(menu_item)

        submenu = gtk.Menu()
        menu_item.set_submenu(submenu)

        self.add_config_menu_items(submenu)
        
        menu_item = gtk.SeparatorMenuItem()
        submenu.append(menu_item)
        
        menu_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu_item.connect('activate', self.on_menuitem_about_activate)
        submenu.append(menu_item)

        menu_item = gtk.ImageMenuItem(_('Go to Web Page'))
        menu_item.set_image(gtk.image_new_from_icon_name(settings.WEB_PAGE_ICON,
                                                     settings.ICON_SIZE))
        menu_item.connect('activate', self.on_menuitem_goto_webpage)
        submenu.append(menu_item)

        menu_item = gtk.SeparatorMenuItem()
        submenu.append(menu_item)
        
        menu_item = gtk.ImageMenuItem(_('Report a Bug'))
        menu_item.set_image(gtk.image_new_from_icon_name(settings.WEB_PAGE_ICON, 
                                                     settings.ICON_SIZE))
        menu_item.connect('activate', self.on_menuitem_bug)
        submenu.append(menu_item)

        menu_item = gtk.ImageMenuItem(_('Help with Translations'))
        menu_item.set_image(gtk.image_new_from_icon_name(settings.WEB_PAGE_ICON, 
                                                     settings.ICON_SIZE))
        menu_item.connect('activate', self.on_menuitem_translations)
        
        submenu.append(menu_item)
        
        menu_item = gtk.ImageMenuItem(_('Donate via Flattr'))
        menu_item.set_image(gtk.image_new_from_icon_name(settings.WEB_PAGE_ICON, 
                                                     settings.ICON_SIZE))
        menu_item.connect('activate', self.on_menuitem_flattr)
        submenu.append(menu_item)

        menu_item = gtk.ImageMenuItem(_('Donate via PayPal'))
        menu_item.set_image(gtk.image_new_from_icon_name(settings.WEB_PAGE_ICON, 
                                                     settings.ICON_SIZE))
        menu_item.connect('activate', self.on_menuitem_donate)
        submenu.append(menu_item)


        menu_item = gtk.SeparatorMenuItem()
        submenu.append(menu_item)

        menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menu_item.connect('activate', self.on_menuitem_quit_activate)
        submenu.append(menu_item)

        menu.show_all()
        return menu;

    def is_unity(self):
        return os.getenv('XDG_CURRENT_DESKTOP', '') == 'Unity'
    
    def create_all_trees(self):
        self.trees = []
        if settings.USE_LENS_MENU and self.is_unity():
            tree = self.create_tree('unity-lens-applications.menu')
            self.trees.append(tree)
        else:
            menu_prefix = os.getenv('XDG_MENU_PREFIX', '')  
            tree = self.create_tree('%sapplications.menu' % menu_prefix)
            self.trees.append(tree)


        for m in settings.SYSTEM_MENUS:
            tree = self.create_tree(m)
            if tree:
                self.trees.append(tree)
                break

        for m in settings.EXTRA_MENUS:
            tree = self.create_tree(m)
            if tree:
                self.trees.append(tree)

    
    def create_tree(self, name):
        flags = gmenu.FLAGS_NONE
        if settings.INCLUDE_NODISPLAY:
            flags = flags | gmenu.FLAGS_INCLUDE_NODISPLAY
        tree = gmenu.lookup_tree(name, flags)
        if tree.get_root_directory():
            tree.add_monitor(self.on_menu_file_changed)
            return tree
        else:
            return None


    def update_menu(self, recreate_trees=False):
        self.notify(_('Updating %s menu. Please wait ...') % settings.APP_NAME)
        self.update_requested = False
        if recreate_trees:
            self.create_all_trees()
        self.indicator.set_menu(self.create_menu())
        print 'DONE'
        self.notify(_('%s is ready now.') % settings.APP_NAME)
        return False    # Don't run again

    def request_update(self, recreate_trees=False):        
        if not self.update_requested:
            self.notify(_('Menu update for %s requested.') % settings.APP_NAME) 
            self.update_requested = True
            gobject.timeout_add(settings.UPDATE_DELAY,
                                lambda: self.update_menu(recreate_trees))
            
    def quit(self):
        gtk.main_quit()


    def open_url(self, url):
        u = urlparse(url)
        appinfo=gio.app_info_get_default_for_uri_scheme(u.scheme)
        appinfo.launch_uris([url])
        
#####################
## Signal-Behandlung
#####################

    def on_config_changed(self):
        self.indicator.set_icon(settings.ICON)
        self.request_update(recreate_trees=True)
        
    def on_menuitem_activate(self, menuitem, entry):
        path = entry.get_desktop_file_path()
        appinfo = gio.unix.desktop_app_info_new_from_filename(path)
        appinfo.launch()

    def on_menu_file_changed(self, tree):
        self.request_update()
        
    def on_menuitem_quit_activate(self, menuitem):
        self.quit()

    def on_menuitem_about_activate(self, menuitem):
        about.show_about_dialog()

    def on_menuitem_docs(self, menuitem):
        self.open_url(settings.LOCAL_DOCS_URL)

    def on_menuitem_goto_webpage(self, menuitem):
        self.open_url(settings.WEB_URL)

    def on_menuitem_donate(self, menuitem):
        self.open_url(settings.PAYPAL_URL)

    def on_menuitem_flattr(self, menuitem):
        self.open_url(settings.FLATTR_URL)

    def on_menuitem_translations(self, menuitem):
        self.open_url(settings.TRANSLATIONS_URL)

    def on_menuitem_bug(self, menuitem):
        self.open_url(settings.BUGREPORT_URL)

def parse_args():
    parser = OptionParser(version="%s %s"%(settings.APP_NAME, 
                                           settings.APP_VERSION))
    (options, args) = parser.parse_args()
    

def main():
    parse_args()
    indicator = ClassicMenuIndicator()
    indicator.run()


    

