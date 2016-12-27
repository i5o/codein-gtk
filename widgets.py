#!/usr/bin/env python

import gi
import json
gi.require_version('Gtk', '3.0')

from gi.repository import Gio
from gi.repository import Gtk

organizations = {
    5382353857806336: "Apertium",
    4814441002565632: "BRL-CAD",
    6426002725011456: "CCExtractor Development",
    4809822100783104: "Copyleft Games",
    5129917289201664: "Drupal",
    6707477701722112: "FOSSASIA",
    5761416665497600: "Haiku Inc",
    5186916471275520: "KDE",
    4794680462016512: "MetaBrainz Foundation",
    5084291717398528: "Mifos Initiative",
    5452182442737664: "MovingBlocks",
    5747383933599744: "OpenMRS",
    5114486142795776: "Sugar Labs",
    5770017069072384: "Sustainable Computing Research Group ( SCoRe )",
    6025234696110080: "Systers, an Anita Borg Institute Community",
    5385807011512320: "Wikimedia",
    4718815233441792: "Zulip"
}


class WindowWithHeader(Gtk.Window):

    def __init__(self, title):
        Gtk.Window.__init__(self)

        self.title_bar = Header(title)
        self.set_titlebar(self.title_bar)
        self.show_all()


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


class TasksList(Gtk.ListBox):

    def __init__(self):
        Gtk.ListBox.__init__(self)

        f = open("tasks.json", "r")
        tasks = json.load(f)['results']
        f.close()

        for task in tasks:
            self.add(TaskInterface(task))


class TaskInterface(Gtk.Box):

    def __init__(self, test_task):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        organization_label = Gtk.Label(
            organizations[
                test_task["organization_id"]].upper())
        organization_label.set_size_request(400, 30)
        organization_label.set_xalign(0)
        organization_label.props.margin_left = 5
        organization_label.props.margin_top = 5

        task_name = Gtk.Label(test_task["name"])
        task_name.set_xalign(0)
        task_name.props.margin_left = 5
        task_name.props.margin_top = 5
        task_name.set_line_wrap(True)

        task_description_expander = Gtk.Expander(label="Description")

        task_description = Gtk.Label(test_task["description"])
        task_description.props.xpad = 30
        task_description.set_yalign(0)
        task_description.set_xalign(0)
        task_description.set_line_wrap(True)

        task_description_expander.add(task_description)

        self.pack_start(organization_label, False, False, 0)
        self.pack_start(task_name, False, False, 0)
        self.pack_end(task_description_expander, True, True, 10)

        """
        button2 = Gtk.Button(label="Button 2")
        button3 = Gtk.Label(label=test_task["name"])
        button4 = Gtk.Button(label=organizations[test_task["organization_id"]])
        button5 = Gtk.Button(label="Button 5")
        button6 = Gtk.Button(label="Button 6")

        self.add(button1)
        self.attach(button2, 1, 0, 2, 1)
        self.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        self.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
        self.attach(button5, 1, 2, 1, 1)
        self.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)
        """

        self.set_size_request(-1, -1)
        self.show_all()


class ScrolledWindow(Gtk.ScrolledWindow):

    def __init__(self, widget):
        Gtk.ScrolledWindow.__init__(self)

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add_with_viewport(widget)
        self.show_all()
