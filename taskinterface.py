#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from widgets import WindowWithHeader


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

        # Title 0/200
        # Description 0/1500
        # Instance count 1/500
        # Days 3-7
        # External url http://[].[min 2]
        # Beginner task
        # Categories
        # 1: Code
        # 2: User Interface
        # 3: Documentation / training
        # 4: Quality Assurance
        # 5: Outreach / Research
        #
        # Tags max 5
