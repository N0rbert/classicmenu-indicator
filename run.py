#!/usr/bin/python
#-*- coding: utf-8 -*-
#

import os.path, sys

fullpath = os.path.abspath(__file__)
path = os.path.split(fullpath)[0]
sys.path=[path]+sys.path

import classicmenu_indicator

classicmenu_indicator.main()
