#!/usr/bin/env python

from gi.repository import Gio
from gi.repository import Gtk


class Header(Gtk.HeaderBar):

    def __init__(self, title):
        Gtk.HeaderBar.__init__(self)

        self.set_show_close_button(True)
        self.set_title(title)


class Button(Gtk.Button):

    def __init__(self, icon_name, tooltip):
        Gtk.Button.__init__(self)

        icon = Gio.ThemedIcon(name=icon_name)
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.add(image)

        Tooltip(self, tooltip)


class Tooltip(Gtk.Popover):

    def __init__(self, button, text):
        Gtk.Popover.__init__(self)

        label = Gtk.Label(label=text)

        button.connect("leave-notify-event", self._hide)
        button.connect("enter-notify-event", self._show)

        self.set_border_width(6)
        self.set_relative_to(button)
        self.set_modal(False)

        self.add(label)

    def _show(self, event, button):
        self.show_all()

    def _hide(self, event, button):
        self.hide()


class Alert(Gtk.InfoBar):

    def __init__(self, text):
        Gtk.InfoBar.__init__(self)

        label = Gtk.Label(label="<b>%s</b>" % text)
        label.set_use_markup(True)
        self.get_content_area().add(label)

        self.set_border_width(8)
        self.set_show_close_button(True)
        self.set_message_type(Gtk.MessageType.ERROR)

    def do_response(self, event):
        self.destroy()
