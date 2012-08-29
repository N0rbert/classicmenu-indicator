#!/usr/bin/env python
#-*- coding: utf-8-*-
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
import gtk, glib, gobject
import appindicator
import re
import textwrap
import subprocess
from optparse import OptionParser
import xdg.IconTheme as xdgicon

import settings, about
from gettext import gettext as _
import gettext

re_command = re.compile('%[UFuf]')
cmd_terminal = 'gnome-terminal -e'

include_nodisplay = False

class ClassicMenuIndicator(object):
    def __init__(self):
        self.indicator = appindicator.Indicator(settings.app_name,
                                                settings.ICON,
                                                settings.category)

        gettext.bindtextdomain(settings.GETTEXT_DOMAIN)
        gettext.textdomain(settings.GETTEXT_DOMAIN)
        gettext.bind_textdomain_codeset(settings.GETTEXT_DOMAIN, 'UTF-8')

        self.icon_size = 22  #like in libindicator:indicator_image_helper.c:refresh_image()

        self.update_requested = False

        self.indicator.set_status (appindicator.STATUS_ACTIVE)

        self.trees = []
        tree = self.create_tree('applications.menu')
        self.trees.append(tree)
        tree = self.create_tree('settings.menu')
        if tree:
            self.trees.append(tree)
        else:
            tree = self.create_tree('classicmenuindicatorsystem.menu')
            self.trees.append(tree)


        self.indicator.set_menu(self.create_menu())

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass



    def create_menu_item(self, entry):    
        icon = entry.get_icon()
        name = entry.get_name()

        menu_item = gtk.ImageMenuItem(name)

        default_theme = gtk.icon_theme_get_default()

        if (icon):
            menu_item = gtk.ImageMenuItem(name)

            try:
                if default_theme.lookup_icon(icon, self.icon_size, 
                                             gtk.ICON_LOOKUP_USE_BUILTIN):
                    pixbuf = default_theme.load_icon(icon, self.icon_size, 
                                                     gtk.ICON_LOOKUP_USE_BUILTIN)
                    if pixbuf.get_height() > self.icon_size:
                        scale = pixbuf.get_height() / float(self.icon_size)
                        width = int(pixbuf.get_width() * scale)
                        pixbuf.scale_simple(width, self.icon_size, gtk.gdk.INTERP_BILINEAR)
                    img = gtk.image_new_from_pixbuf(pixbuf)
                else:
                    icon_path = xdgicon.getIconPath(icon)
                    if icon_path:
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon_path, 
                                                                      self.icon_size,
                                                                      self.icon_size)
                        img = gtk.image_new_from_pixbuf(pixbuf)
                    else:
                        img = gtk.Image()                    
                        img.set_from_icon_name(icon, self.icon_size)

            except glib.GError, e:
                print '[%s] %s: %s'%(settings.APP_NAME, icon , e)
                img = gtk.Image()
                img.set_from_icon_name('', self.icon_size)
 
            menu_item.set_image(img)
            menu_item.set_always_show_image(True)
        else:
            menu_item = gtk.MenuItem(name) 
           
        if entry.get_type() ==  gmenu.TYPE_ENTRY:
            menu_item.connect('activate', self.on_menuitem_activate, entry)

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

        menu_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu_item.connect('activate', self.on_menuitem_about_activate)
        submenu.append(menu_item)
        
        menu_item = gtk.ImageMenuItem(_('Web page'))
        menu_item.connect('activate', self.on_menuitem_goto_webpage)
        submenu.append(menu_item)
        
        menu_item = gtk.ImageMenuItem(_('Donate'))
        menu_item.connect('activate', self.on_menuitem_donate)
        submenu.append(menu_item)

        menu_item = gtk.SeparatorMenuItem()
        submenu.append(menu_item)

        menu_item = gtk.ImageMenuItem(settings.APP_NAME)
        menu_item.connect('activate', self.on_menuitem_quit_activate)
        submenu.append(menu_item)

        menu.show_all()
        return menu;

    def create_tree(self, name):
        flags = gmenu.FLAGS_NONE
        if include_nodisplay:
            flags = flags | gmenu.FLAGS_INCLUDE_NODISPLAY
        tree = gmenu.lookup_tree(name, flags)
        if tree.get_root_directory():
            tree.add_monitor(self.on_menu_file_changed)
            return tree
        else:
            return None


    def update_menu(self):
        self.update_requested = False
        self.indicator.set_menu(self.create_menu())        
        return False    # Don't run again

    def quit(self):
        gtk.main_quit()

#####################
## Signal-Behandlung
#####################

    def on_menuitem_activate(self, menuitem, entry):
        command = entry.get_exec()
        if command:        
            command=re_command.sub('', command)
            if entry.get_launch_in_terminal():
                command = '%s %s' % (cmd_terminal, command)
            p=subprocess.Popen(command, shell=False)

    def on_menu_file_changed(self, tree):
        if not self.update_requested:
            self.update_requested = True
            gobject.timeout_add(5000, self.update_menu)
   
    def on_menuitem_quit_activate(self, menuitem):
        self.quit()

    def on_menuitem_about_activate(self, menuitem):
        about.show_about_dialog()

    def on_menuitem_goto_webpage(self, menuitem):
        url = settings.WEB_URL
        command = 'xdg-open %s' % (url)
        p=subprocess.Popen(command, shell=True)

    def on_menuitem_donate(self, menuitem):
        command = "xdg-open '%s'" % (settings.PAYPAL_URL)
        p=subprocess.Popen(command, shell=True)

def parse_args():
    parser = OptionParser(version="%s %s"%(settings.APP_NAME, 
                                           settings.APP_VERSION))
    (options, args) = parser.parse_args()
    

def main():
    parse_args()
    indicator = ClassicMenuIndicator()
    indicator.run()   

if __name__ == '__main__':
    main ()
    
