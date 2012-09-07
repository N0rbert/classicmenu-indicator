#!/usr/bin/env python
#-*- coding: utf-8 -*-
# classicmenu-indicator - an indicator showing the main menu from Gnome Classic
#
# Copyright (C) 2011 Florian Diesch <devel@florian-diesch.de>
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

import glob

import distribute_setup
distribute_setup.use_setuptools()

from setup_helpers import (
    description, find_doctests, get_version, long_description, require_python)
from setuptools import setup, find_packages

from DistUtilsExtra.command import *

from deb_setup_helpers import (get_deb_version, get_deb_description, 
                               create_version_module)

require_python(0x20600f0)


create_version_module('classicmenu_indicator')


setup(
    name='classicmenu-indicator',
    version=get_deb_version(full=False),
    packages=find_packages(),
    include_package_data=True,
    maintainer='Florian Diesch',
    maintainer_email='devel@florian-diesch.de',
    author = "Florian Diesch",
    author_email = "devel@florian-diesch.de",    
    description=get_deb_description(),
    long_description=long_description(
        'README.txt'       
        ),
    data_files=[
        ('bin',
         glob.glob('bin/*')),
        ('/usr/share/applications',
         glob.glob('data/desktop/*.desktop')),
        ('/etc/xdg/autostart',
         glob.glob('data/desktop/classicmenu-indicator.desktop')),
        ('/etc/xdg/menus',
         glob.glob('data/menu/*.menu')),
        ('/usr/share/icons/hicolor/22x22/apps',
         ('data/icons/classicmenu-indicator.png',)),
        ],
    license='GPLv3',
    url='http://www.florian-diesch.de/software/classicmenu-indicator/',
    download_url='http://www.florian-diesch.de/software/classicmenu-indicator/',
    keywords = "Ubuntu, Unity, Indicator, Applet, Gnome, menu, Classic Menu", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Gnome',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Utilities',
        ],
    cmdclass = { "build" : build_extra.build_extra,
                 "build_i18n" :  build_i18n.build_i18n,
                 "build_help" :  build_help.build_help,
                 "build_icons" :  build_icons.build_icons }

    )
