#!/usr/bin/env python

import gi
import json
gi.require_version('Gtk', '3.0')

from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


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


TAGS = {1: ["img/code.svg", "Code"],
        2: ["img/userinterface.svg", "User Interface"],
        3: ["img/doc.svg", "Documentation / Training"],
        4: ["img/qa.svg", "Quality Assurance"],
        5: ["img/outreach.svg", "Outearch / Research"]
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
        self.limit = 0
        self.total_tasks = 0
        self.showed_tasks = []
        self.add_tasks()

    def add_tasks(self):
        f = open("tasks.json", "r")
        tasks = json.load(f)['results']
        f.close()
        self.limit += 25
        self.total_tasks = len(tasks)

        for task in tasks:
            if task in self.showed_tasks:
                continue

            if len(self.showed_tasks) > self.limit:
                if len(self.showed_tasks) < self.total_tasks:
                    widget = ShowMoreTasks(self)
                self.add(widget)
                break

            self.add(TaskInterface(task))
            self.showed_tasks.append(task)

        if len(self.showed_tasks) == self.total_tasks:
            widget = ShowMoreTasks(self, True)
            self.add(widget)


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

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.pack_start(organization_label, False, False, 0)
        header.pack_end(
            Icon(
                days=test_task["time_to_complete_in_days"]),
            False,
            False,
            5)

        for cat in test_task["categories"]:
            header.pack_end(Icon(category=cat), False, False, 5)

        self.pack_start(header, False, False, 0)
        self.pack_start(task_name, False, False, 0)
        self.pack_end(task_description_expander, True, True, 10)

        self.show_all()


class ScrolledWindow(Gtk.ScrolledWindow):

    def __init__(self, widget):
        Gtk.ScrolledWindow.__init__(self)

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add_with_viewport(widget)
        self.show_all()


class Icon(Gtk.EventBox):

    def __init__(self, category=None, scale=24, days=0):
        Gtk.EventBox.__init__(self)

        img = Gtk.Image()
        if category:
            path = TAGS[category][0]
            Tooltip(self, TAGS[category][1])
        elif days > 1:
            path = "img/time.svg"
            Tooltip(self, "%d days" % days)
        else:
            return "Error."

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            path, scale, scale, True)
        img.set_from_pixbuf(pixbuf)
        self.add(img)
        self.show_all()


class ShowMoreTasks(Gtk.EventBox):

    def __init__(self, tasks_list, last=False):
        Gtk.EventBox.__init__(self)
        self.tasks_list = tasks_list

        self.label = Gtk.Label()
        if not last:
            self.label.set_text(
                "Show more (+25) tasks!\n<i>-The application may work slowly</i>-\n(Double click)")
            self.label.set_use_markup(True)
            self.label.set_justify(Gtk.Justification.CENTER)
            self._id = self.connect("button-press-event", self.button_press)

        if last:
            self.label.set_text("End of the list. :(")
            self.set_sensitive(False)

        self.add(self.label)
        self.show_all()

    def button_press(self, widget, event):
        if event.type == 5:
            self.disconnect(self._id)
            self.label.set_text(
                "%d/%d" %
                (len(
                    self.tasks_list.showed_tasks),
                    self.tasks_list.total_tasks))
            self.set_sensitive(False)
            self.tasks_list.add_tasks()
