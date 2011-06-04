#!/usr/bin/env python
#-*- coding: utf-8-*-
#
# classicmenu-indicator - an indicator showing the main menu from Gnome Classic
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
import gobject
import gtk
import appindicator
import re
import subprocess


APP_NAME = 'ClassicMenu Indicator'

re_command = re.compile('%[UFuf]')
cmd_terminal = 'gnome-terminal -e'


def on_menuitem_activate(menuitem, entry):
    command = entry.get_exec()
    if command:        
        command=re_command.sub('', command)
        if entry.get_launch_in_terminal():
            command = '%s %s' % (cmd_terminal, command)
        subprocess.Popen(command, shell=True)


def create_menu_item(entry):
    
    icon = entry.get_icon()
    name = entry.get_name()

    menu_item = gtk.ImageMenuItem(name)

    if (icon):
        menu_item = gtk.ImageMenuItem(name)
        img =  gtk.Image()

        if icon.startswith('/'):
            img.set_from_file(icon)
        else:
            img.set_from_icon_name(icon, 64)

        menu_item.set_image(img)
        menu_item.set_always_show_image(True)
    else:
       menu_item = gtk.MenuItem(name) 
           
    if entry.get_type() ==  gmenu.TYPE_ENTRY:
        menu_item.connect('activate', on_menuitem_activate, entry)

    menu_item.show()    
    return menu_item


def process_entry(menu, entry):
    menu.append(create_menu_item(entry))

    
def process_directory(menu, dir):
    if dir:
        for item in dir.get_contents():
            type = item.get_type()
            if type == gmenu.TYPE_ENTRY:
                process_entry(menu, item)
            elif type == gmenu.TYPE_DIRECTORY:
                new_menu = gtk.Menu()
                menu_item = create_menu_item(item)
                menu_item.set_submenu(new_menu)
                menu.append(menu_item)
                menu_item.show()
                process_directory(new_menu, item)
            elif type == gmenu.TYPE_ALIAS:
                aliased = item.get_item()
                if aliased.get_type() == gmenu.TYPE_ENTRY:
                    process_entry(menu, aliased)
            elif type == gmenu.TYPE_SEPARATOR:
                menu_item = gtk.SeparatorMenuItem()
                menu.append(menu_item)
                menu_item.show()
            elif type in [ gmenu.TYPE_HEADER ]:
                pass
            else:
                print >> sys.stderr, 'Unsupported item type: %s' % type



def on_menu_changed(tree, ind):
    ind.set_menu(create_menu(tree))

def create_menu(tree):
    menu = gtk.Menu()
    root = tree.get_root_directory()    
    process_directory(menu, root)
    return menu;

def create_tree(ind):
    menu_file = 'applications.menu'
    flags = gmenu.FLAGS_NONE
    tree = gmenu.lookup_tree(menu_file, flags)
    tree.add_monitor(on_menu_changed, ind)
    return tree

def create_indicator():
    ind = appindicator.Indicator ("classicmenu-indicator",
                                  "start-here",
                                  appindicator.CATEGORY_SYSTEM_SERVICES)
    ind.set_status (appindicator.STATUS_ACTIVE)
    return ind;


def main():
    ind = create_indicator()    
    tree = create_tree(ind)
    menu = create_menu(tree)
    ind.set_menu(menu)
    gtk.main()


if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
      pass
