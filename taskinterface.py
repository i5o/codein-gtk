#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from widgets import Header, Button, WindowWithHeader


class NewTaskWindow(WindowWithHeader):

    def __init__(self, parent):
        WindowWithHeader.__init__(self, "Add new task")

        self.set_destroy_with_parent(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_transient_for(parent)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_size_request(640, 480)
        self.show_all()
