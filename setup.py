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

import distribute_setup
distribute_setup.use_setuptools()

from setup_helpers import (
    description, find_doctests, get_version, long_description, require_python)
from setuptools import setup, find_packages


require_python(0x20600f0)
__version__ = get_version('classicmenu_indicator/__init__.py', r'(?P<version>\d+\.\d+(?:\.\d+)?)')


setup(
    name='classicmenu-indicator',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    maintainer='Florian Diesch',
    maintainer_email='devel@florian-diesch.de',
    description=description('README.txt'),
    long_description=long_description(
        'README.txt',
        'NEWS.txt',
        ),
    license='GPLv3',
    url='http://www.florian-diesch.de/software/classicmenu-indicator/',
    download_url='http://www.florian-diesch.de/software/classicmenu-indicator/',
    install_requires = [
        ],
    entry_points = {
        'console_scripts': ['classicmenu-indicator=classicmenu_indicator:main'],
        },
    )
