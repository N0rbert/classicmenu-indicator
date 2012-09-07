#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import xdg.BaseDirectory


class Config(object):

    def __init__(self, *files):
        self.section = 'config'
        try:
            self.parser = ConfigParser.SafeConfigParser()
            self.parser.read(*files)
        except ConfigParser.Error as e:
            print e
    
    def get(self, key, default, _type=str):
        try:
            if _type == int:
                return self.parser.getint(self.section, key)
            elif _type == float:
                return self.parser.getfloat(self.section, key)
            elif type == bool:
                return self.parser.getbool(self.section, key)
            else:
                return self.parser.get(self.section, key, raw=True)



        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            return default
        except ConfigParser.Error as e:
            print e, type(e)
            return default



    
if __name__ == '__main__':
    import os.path
    app_name = 'classicmenu-indicator'
    cfg = Config(os.path.expanduser('~/.config/%s/config' % app_name))
    print cfg.get('icon', 'classicmenu-indicator')

    


