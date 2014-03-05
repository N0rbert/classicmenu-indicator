#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import xdg.BaseDirectory
import gio

class Config(object):

    def __init__(self, save_to, *files):
        self.files = files
        self.save_to = save_to
        self.callback = None
        self.section = 'config'                
        self.monitors = [self.create_monitor(f) for f in files]
        self.load()

    def set_callback(self, callback):
        self.callback = callback
        
    def create_monitor(self, path):
        gfile = gio.File(path)
        monitor = gfile.monitor(0, None)
        monitor.connect('changed', self.on_file_changed)
        return monitor
        
    def load(self):
        try:
            self.parser = ConfigParser.SafeConfigParser()
            self.parser.read(*self.files)
        except ConfigParser.Error as e:
            print e
            
        if self.callback is not None:
            self.callback()

    def store(self):
        try:
            with open(self.save_to, 'w') as saveto:
                self.parser.write(saveto)
        except OSError as e:
            print e
                
    def set(self, key, value):
        value = str(value)
        self.parser.set(self.section, key, value)
        
    def get(self, key, default, _type=None):
        if _type is None:            
            _type=type(default)
        try:
            if _type == int:
                return self.parser.getint(self.section, key)
            elif _type == float:
                return self.parser.getfloat(self.section, key)
            elif _type == bool:
                return self.parser.getboolean(self.section, key)
            else:
                return self.parser.get(self.section, key, raw=True)



        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            return default
        except ConfigParser.Error as e:
            print e, type(e)
            return default

    def on_file_changed(self, monitor, gfile, other, event):
        if event in (gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT,
                     gio.FILE_MONITOR_EVENT_DELETED):                
            self.load()
    
if __name__ == '__main__':
    import os.path
    app_name = 'classicmenu-indicator'
    cfg = Config(os.path.expanduser('~/.config/%s/config' % app_name))
    print cfg.get('icon', 'classicmenu-indicator')

    


