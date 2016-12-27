#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from widgets import Button, WindowWithHeader, TasksList, ScrolledWindow, SearchButton, SearchBar
from taskinterface import NewTaskWindow


class Window(WindowWithHeader):

    def __init__(self):
        WindowWithHeader.__init__(self, "GCI 2016 Tasks")

        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        add_task_button = Button("list-add", "Add task")
        add_task_button.connect("clicked", self._add_task)
        self.title_bar.pack_start(add_task_button)

        tasks = TasksList()

        search_bar = SearchBar()
        search_button = SearchButton(search_bar, tasks)
        self.title_bar.pack_end(search_button)

        self.content.pack_start(search_bar, False, False, 0)
        self.content.pack_end(ScrolledWindow(tasks), True, True, 0)

        self.add(self.content)
        self.set_resizable(False)
        self.set_size_request(1024, 768)
        self.connect("delete-event", Gtk.main_quit)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.show_all()

    def _add_task(self, button):
        NewTaskWindow(self)


if __name__ == "__main__":
    Window()
    Gtk.main()
