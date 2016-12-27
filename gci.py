#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from widgets import Button, WindowWithHeader, TasksList, ScrolledWindow
from taskinterface import NewTaskWindow


class Window(WindowWithHeader):

    def __init__(self):
        WindowWithHeader.__init__(self, "GCI 2016 Tasks")

        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        add_task_button = Button("list-add", "Add task")
        add_task_button.connect("clicked", self._add_task)
        self.title_bar.add(add_task_button)

        tasks = TasksList()
        self.content.pack_end(tasks, True, True, 0)

        self.add(ScrolledWindow(self.content))
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
