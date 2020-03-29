#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# ClassicMenu Indicator - classicmenu-indicator
# http://www.florian-diesch.de/software/classicmenu-indicator/
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

import glob
from setuptools import setup, find_packages


setup(
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('share/man/man1',
         glob.glob('data/man/*.1')),
        ('share/applications',
         glob.glob('data/desktop/*.desktop')),
        ('share/classicmenu-indicator/ui/',
         glob.glob('data/ui/*.ui')),
        ('share/classicmenu-indicator/',
         glob.glob('data/menu/*.menu')),
        ('share/icons/hicolor/scalable/apps',
         glob.glob('data/icons/hicolor/scalable/apps/*.svg')),
        ('share/icons/ubuntu-mono-light/status/22',
         glob.glob('data/icons/ubuntu-mono-light/status/22/*.svg')),
        ('share/icons/ubuntu-mono-light/status/24',
         glob.glob('data/icons/ubuntu-mono-light/status/24/*.svg')),
        ('share/icons/ubuntu-mono-light/status/16',
         glob.glob('data/icons/ubuntu-mono-light/status/16/*.svg')),
        ('share/icons/ubuntu-mono-dark/status/22',
         glob.glob('data/icons/ubuntu-mono-dark/status/22/*.svg')),
        ('share/icons/ubuntu-mono-dark/status/24',
         glob.glob('data/icons/ubuntu-mono-dark/status/24/*.svg')),
        ('share/icons/ubuntu-mono-dark/status/16',
         glob.glob('data/icons/ubuntu-mono-dark/status/16/*.svg')),
    ],
    entry_points={
        'console_scripts': ['classicmenu-indicator=classicmenu_indicator:main'],
    },
    keywords="Ubuntu, Unity, Indicator, Menu, System Tray, Tray Icon, Applet, Classic Menu",
    python_requires=">=3.0",
    zip_safe=False,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: X11 Applications :: Gnome',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Desktop Environment',
        'Topic :: Utilities',
    ],
)
