# -*- coding: utf-8 -*-


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

import os
import os.path
from gettext import gettext as _
from gi.repository import Gtk
from .settings import (vars as settings, get_all_menu_files,
                       get_default_menu_files)
from . import tvtools, dialogs


class PreferencesDlg:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(settings.GETTEXT_DOMAIN)

        gladefile = os.path.join(settings.UI_DIR, 'preferences.ui')
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(self)

        self.setup_tvs()
        self.setup_menus_intro()

    def setup_tvs(self):
        tv = self['tv_menus_avail']
        model_avail = Gtk.ListStore(str)
        model_avail.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        tv.set_model(model_avail)
        tvtools.create_treeview_column(tv, 'Unused Menus', col_no=0)

        tv = self['tv_menus_used']
        model_used = Gtk.ListStore(str)
        tv.set_model(model_used)
        tvtools.create_treeview_column(tv, 'Used Menus', col_no=0)

        self.load()

    def setup_menus_intro(self):
        default = get_default_menu_files()
        if default:
            intro = 'Your standard menu seems to be "{default}".'

        else:
            intro = "It seems there is no standard menu for your current "\
                    " desktop environment. Choose any of the menus from below"
            self['b_default_menus'].set_sensitive(False)

        intro = intro.format(default=', '.join(default))

        self['l_menus_intro_default'].set_text(intro)

    def get_unused_menus(self):
        model = self['tv_menus_avail'].get_model()
        return [r[0] for r in model]

    def get_used_menus(self):
        model = self['tv_menus_used'].get_model()
        return [r[0] for r in model]

    def set_used_menus(self, menus):
        model = self['tv_menus_used'].get_model()
        model.clear()
        for m in menus:
            model.append([m])

        model = self['tv_menus_avail'].get_model()
        unused = [m for m in get_all_menu_files() if m not in menus]
        model.clear()
        for m in unused:
            model.append([m])

    def set_default_menus(self):
        default_menu = get_default_menu_files()
        self.set_used_menus(default_menu)

    def load(self):
        self.set_used_menus(settings.MENUS)
        self['sw_settings_icons'].set_active(settings.USE_MENU_ICONS)
        self['sw_settings_show_hidden'].set_active(settings.INCLUDE_NODISPLAY)
        self['sw_settings_extra_menus'].set_active(settings.USE_EXTRA_MENUS)
        self['sw_settings_all_apps_menu'].set_active(
            settings.USE_ALL_APPS_MENU)
        self['sw_settings_tooltips'].set_active(settings.USE_TOOLTIPS)
        self['sw_settings_remove_duplicates'].set_active(
            settings.REMOVE_DUPLICATES)

        self['sw_folder_menu_needs_terminal'].set_active(
            settings.FOLDER_MENU_NEEDS_TERMINAL)
        self['e_folder_menu_root'].set_text(settings.FOLDER_MENU_ROOT)

        _icons = {v: k for k, v in settings.ICONS.items()}
        if settings.ICON in _icons:
            self['cbox_icon'].set_active_id(_icons[settings.ICON])
        else:
            self['cbox_icon'].set_active_id('custom')
            self['fcb_icon'].set_filename(settings.ICON)

    def save(self):
        settings.MENUS = self.get_used_menus()
        settings.USE_MENU_ICONS = self[
            'sw_settings_icons'].get_active()
        settings.INCLUDE_NODISPLAY = self[
            'sw_settings_show_hidden'].get_active()
        settings.USE_EXTRA_MENUS = self[
            'sw_settings_extra_menus'].get_active()
        settings.USE_ALL_APPS_MENU = self[
            'sw_settings_all_apps_menu'].get_active()
        settings.USE_TOOLTIPS = self[
            'sw_settings_tooltips'].get_active()
        settings.REMOVE_DUPLICATES = self[
            'sw_settings_remove_duplicates'].get_active()
        settings.FOLDER_MENU_NEEDS_TERMINAL = self[
            'sw_folder_menu_needs_terminal'].get_active()
        settings.FOLDER_MENU_ROOT = self[
            'e_folder_menu_root'].get_text()
        icon_mode = self[
            'cbox_icon'].get_active_id()

        if icon_mode in settings.ICONS:
            settings.ICON = settings.ICONS[icon_mode]
        else:
            fname = self['fcb_icon'].get_filename()
            if fname:
                settings.ICON = fname
        try:
            settings.save()
        except IOError as e:
            dialogs.error(self['dialog'], "Can't save preferences",
                          str(e))

    def __getitem__(self, key):
        return self.builder.get_object(key)

    def run(self):
        dlg = self['dialog']
        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            self.save()
            result = True
        else:
            result = False
        dlg.destroy()
        return result

    def move_current_tv_row(self, tv_a, tv_b):
        row = tvtools.get_current_row(tv_a)
        if row:
            menu = row[0]
            model_b = tv_b.get_model()
            if menu not in model_b:
                model_b.append([menu])
                tvtools.del_current_row(tv_a)

    def on_b_set_defaults_clicked(self, *args):
        settings.set_to_defaults()
        self.load()

    def on_b_default_menus_clicked(self, *args):
        self.set_default_menus()

    def on_b_add_clicked(self, *args):
        self.move_current_tv_row(self['tv_menus_avail'],
                                 self['tv_menus_used'])

    def on_b_remove_clicked(self, *args):
        self.move_current_tv_row(self['tv_menus_used'],
                                 self['tv_menus_avail'])

    def on_b_menus_down_clicked(self, *args):
        tv = self['tv_menus_used']
        path, column = tv.get_cursor()
        if path is not None:
            model = tv.get_model()
            iter = model.get_iter(path)
            new = model.iter_next(iter)
            if new:
                model.move_after(iter, new)

    def on_b_menus_up_clicked(self, *args):
        tv = self['tv_menus_used']
        path, column = tv.get_cursor()
        if path is not None:
            model = tv.get_model()
            iter = model.get_iter(path)
            new = model.iter_previous(iter)
            if new:
                model.move_before(iter, new)

    def on_cbox_icon_changed(self, *args):
        cbox = self['cbox_icon']
        fcb = self['fcb_icon']
        cbox_id = cbox.get_active_id()
        fcb.set_sensitive(cbox_id == 'custom')

    def on_b_folder_menu_root_clicked(self, *args):
        dialog = Gtk.FileChooserDialog(
            _('Select folder'), self['dialog'],
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL,
             Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN,
             Gtk.ResponseType.OK))
        response = dialog.run()
        path = dialog.get_filename()
        dialog.destroy()
        if response != Gtk.ResponseType.OK:
            return
        self['e_folder_menu_root'].set_text(path)
