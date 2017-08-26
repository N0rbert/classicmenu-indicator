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


def add_cell_renderer(control, col_no=0, renderer=None, attr='text'):
    if renderer is None:
        renderer = Gtk.CellRendererText()
    control.pack_start(renderer, True)
    control.add_attribute(renderer, attr, col_no)


def create_treeview_column(widget, title, col_no, renderer=None,
                           attr='text', activatable=False):
    column = Gtk.TreeViewColumn(title)
    widget.append_column(column)
    if activatable:
        renderer.set_activatable(True)
    add_cell_renderer(column, col_no, renderer, attr)


def get_current_row(treeview):
    path, column = treeview.get_cursor()
    if path is not None:
        model = treeview.get_model()
        return model[path]


def set_current_row(treeview, row):
    path, column = treeview.get_cursor()
    if path is None:
        append_row(treeview, row)
    else:
        model = treeview.get_model()
        model[path] = row


def del_current_row(treeview):
    path, column = treeview.get_cursor()
    if path is not None:
        model = treeview.get_model()
        del model[path]


def append_row(treeview, row):
    model = treeview.get_model()
    iter_ = model.append(row)
    path = model.get_path(iter_)
    treeview.set_cursor(path)
