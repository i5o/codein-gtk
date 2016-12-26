#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from widgets import Header, Button, WindowWithHeader


class Window(WindowWithHeader):

    def __init__(self):
        WindowWithHeader.__init__(self, "GCI 2016 Tasks")

        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.title_bar.add(Button("list-add", "Add task"))

        self.add(self.content)
        self.set_resizable(False)
        self.set_size_request(1024, 768)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    Window()
    Gtk.main()
