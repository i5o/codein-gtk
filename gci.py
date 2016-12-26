#!/usr/bin/env python

from gi.repository import Gtk
from widgets import Header, Button


class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        title_bar = Header()
        title_bar.add(Button("list-add", "Add task"))
        self.set_titlebar(title_bar)

        self.add(self.content)
        self.set_resizable(False)
        self.set_size_request(1024, 768)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    Window()
    Gtk.main()
