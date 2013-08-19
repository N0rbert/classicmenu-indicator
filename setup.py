#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# ClassicMenu Indicator - classicmenu-indicator
#                    http://www.florian-diesch.de/software/classicmenu-indicator/
#
# Copyright (C) 2013 Florian Diesch <devel@florian-diesch.de>
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

import glob, sys

from setuptools import setup, find_packages

try:
    from DistUtilsExtra.command import *
except ImportError:
    print >> sys.stderr, 'To build ClassicMenu Indicator you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)


def read_from_file(path):
    with open(path) as input:
        return input.read()

import classicmenu_indicator._meta as _meta
    

setup(
    name='classicmenu-indicator',
    version=_meta.VERSION,
    packages=find_packages(),
    include_package_data=True,
    maintainer='Florian Diesch',
    maintainer_email='devel@florian-diesch.de',
    author = "Florian Diesch",
    author_email = "devel@florian-diesch.de",    
    description='classicmenu-indicator',
    long_description=read_from_file('README.txt'),
    data_files=[
        ('/usr/share/applications',
         glob.glob('data/desktop/*.desktop')),
        ('share/classicmenu-indicator/ui/',
         glob.glob('data/ui/*.ui')),
        ('/usr/share/icons/hicolor/scalable/apps',
         glob.glob('icons/hicolor/scalable/apps/*.svg')),
        ('/usr/share/icons/ubuntu-mono-light/status/22',
           glob.glob('icons/ubuntu-mono-light/status/22/*.svg')),
        ('/usr/share/icons/ubuntu-mono-light/status/24',
           glob.glob('icons/ubuntu-mono-light/status/24/*.svg')),
        ('/usr/share/icons/ubuntu-mono-light/status/16',
           glob.glob('icons/ubuntu-mono-light/status/16/*.svg')),
        ('/usr/share/icons/ubuntu-mono-dark/status/22',
           glob.glob('icons/ubuntu-mono-dark/status/22/*.svg')),
        ('/usr/share/icons/ubuntu-mono-dark/status/24',
           glob.glob('icons/ubuntu-mono-dark/status/24/*.svg')),
        ('/usr/share/icons/ubuntu-mono-dark/status/16',
           glob.glob('icons/ubuntu-mono-dark/status/16/*.svg')),
        ],
    entry_points = {
        'console_scripts': ['classicmenu-indicator=classicmenu_indicator:main'],
        },
    license='GPLv3',
    url='http://www.florian-diesch.de/software/classicmenu-indicator/',
    download_url='http://www.florian-diesch.de/software/classicmenu-indicator/',
    keywords = "", 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        ],
    cmdclass = { "build" : build_extra.build_extra,
                 "build_i18n" :  build_i18n.build_i18n,
                 "build_help" :  build_help.build_help,
                 "build_icons" :  build_icons.build_icons }

    )
