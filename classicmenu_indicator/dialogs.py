# -*- coding: utf-8 -*-
#
# Dalp - dalp
# http://www.florian-diesch.de/software/dalp/
#
# Copyright (C) 2015 Florian Diesch <devel@florian-diesch.de>
#
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


from gi.repository import Gtk

from gettext import gettext as _


def yes_no_cancel_question(title, text, parent):
    dlg = Gtk.MessageDialog(parent, 0, Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.NONE,
                            text
                            )
    dlg.set_title(title)
    dlg.add_buttons(
        Gtk.STOCK_YES, Gtk.ResponseType.YES,
        Gtk.STOCK_NO, Gtk.ResponseType.NO,
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
    )
    result = dlg.run()
    dlg.destroy()
    return result


def confirm(title, text, parent):
    dlg = Gtk.MessageDialog(parent, 0, Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.NONE,
                            text
                            )
    dlg.set_title(title)
    dlg.add_buttons(
        Gtk.STOCK_OK, Gtk.ResponseType.OK,
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
    )
    result = dlg.run()
    dlg.destroy()
    return result == Gtk.ResponseType.OK


def information(parent, title, text):
    dlg = Gtk.MessageDialog(parent, 0, Gtk.MessageType.INFO,
                            Gtk.ButtonsType.OK,
                            text
                            )
    dlg.set_title(title)
    result = dlg.run()
    dlg.destroy()
    return result


def error(parent, title, text):
    dlg = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK,
                            text
                            )
    dlg.set_title(title)
    result = dlg.run()
    dlg.destroy()
    return result


def ask_for_value(parent, title, msg, default):
    dlg = Gtk.Dialog(title=title)
    dlg.add_buttons(
        Gtk.STOCK_OK, Gtk.ResponseType.OK,
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
    )
    box = Gtk.HBox()
    dlg.get_content_area().pack_start(box, True, True, 0)
    label = Gtk.Label('{}: '.format(msg))
    box.pack_start(label, True, True, 0)
    entry = Gtk.Entry()
    box.pack_end(entry, True, True, 0)
    entry.set_text(default)
    box.show_all()

    response = dlg.run()
    text = entry.get_text()
    dlg.destroy()

    if response == Gtk.ResponseType.OK:
        return text
    else:
        return default


def ask_for_file_name(title, parent,
                      action=Gtk.FileChooserAction.SAVE,
                      default_ext=None,
                      overwrite_confirmation=True,
                      filters=()):
    if action == Gtk.FileChooserAction.SAVE:
        ok_button = Gtk.STOCK_SAVE
    elif action == Gtk.FileChooserAction.OPEN:
        ok_button = Gtk.STOCK_OPEN
    else:  # CREATE_FOLDER, SELECT_FOLDER
        ok_button = Gtk.STOCK_OPEN

    dialog = Gtk.FileChooserDialog(title, parent, action,
                                   (Gtk.STOCK_CANCEL,
                                    Gtk.ResponseType.CANCEL,
                                    ok_button,
                                    Gtk.ResponseType.OK))
    for name, ext in filters:
        filter = Gtk.FileFilter()
        filter.set_name(name)
        filter.add_pattern('*.%s' % ext)
        dialog.add_filter(filter)

    filter = Gtk.FileFilter()
    filter.set_name(_("Any files"))
    filter.add_pattern("*")
    dialog.add_filter(filter)

    dialog.set_do_overwrite_confirmation(overwrite_confirmation)
    response = dialog.run()
    path = dialog.get_filename()
    dialog.destroy()

    if response != Gtk.ResponseType.OK:
        return

    if default_ext is not None and '.' not in path:
            path = '.'.join((path, default_ext))

    return path
