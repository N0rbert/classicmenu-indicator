# -*- coding: utf-8 -*-

from gi.repository import Gtk

from gettext import gettext as _
import textwrap

from .settings import vars as settings


def show_about_dialog():
    dlg = Gtk.AboutDialog()
    dlg.set_program_name(settings.APP_NAME)
    dlg.set_version(settings.APP_VERSION)
    dlg.set_logo_icon_name(settings.ICONS['auto'])
    dlg.set_website(settings.WEB_URL)
    dlg.set_authors([settings.AUTHOR_EMAIL])
    dlg.set_wrap_license(True)
    dlg.set_copyright('Copyright (c) 2011-2016 %s' % settings.AUTHOR_NAME)
    dlg.set_translator_credits(_("translator-credits"))
    dlg.set_license(textwrap.dedent(
        """
        ClassicMenu Indicator - an indicator showing an app menu like in
                                Gnome Classic
        Copyright (c) 2011-2016 Florian Diesch <devel@florian-diesch.de>

        Homepage: http://www.florian-diesch.de/software/classicmenu-indicator/

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
        """))

    dlg.run()
    dlg.destroy()
