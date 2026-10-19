#!/usr/bin/python3

import datetime
import os
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

APP_ID = "com.enocc.CountdownMachine"

UI_FILE = os.path.join(
	os.path.dirname(os.path.abspath(__file__)),
	"..", "..", "share", "countdown-machine", "countdown-machine.ui",
	)

VERSION = "1.0.0"

class CountdownMachine(Gtk.Application):
	def __init__(self):
		super().__init__(application_id=APP_ID)
		self.window = None
		
		self.settings = Gio.Settings(schema_id=APP_ID)
		self.settings.connect("changed", self.on_settings_changed)
		self.load_settings()

	def load_settings(self):
		self.target_name = self.settings.get_string("target-name")

		value = self.settings.get_string("target-date")
		try:
			self.target_date = datetime.date.fromisoformat(value)
		except ValueError:
			self.target_date = None

	def on_settings_changed(self, settings, key):
		self.load_settings()
		if self.window is not None:
			self.update_label()

	def do_activate(self):
		if self.window is None:
			builder = Gtk.Builder()
			builder.add_from_file(UI_FILE)

			self.window = builder.get_object("main_window")
			self.window.set_application(self)

			# Main Window
			self.countdown_label = builder.get_object("countdown_label")
			self.date_label = builder.get_object("date_label")

			# Preferences Window
			self.prefs_dialog = builder.get_object("prefs_dialog")
			self.event_entry = builder.get_object("event_entry")
			self.date_calendar = builder.get_object("date_calendar")

			# About Dialog
			self.about_dialog = builder.get_object("about_dialog")
			self.about_dialog.set_version(VERSION)

			builder.get_object("prefs_menuitem").connect("activate", self.on_preferences)
			builder.get_object("quit_menuitem").connect("activate", self.on_quit)
			builder.get_object("help_menuitem").connect("activate", self.on_help)

			self.update_label()

		self.window.present()

	def update_label(self):
		if self.target_date is None:
			self.countdown_label.set_text("No date set")
			self.date_label.set_text("Set a date in File -> Preferences")
			return

		days = (self.target_date - datetime.date.today()).days

		if days > 1:
			self.countdown_label.set_text(f"{days} days")
		elif days == 1:
			self.countdown_label.set_text("1 day")
		elif days == 0:
			self.countdown_label.set_text("Today!")
		else:
			self.countdown_label.set_text(f"{abs(days)} days ago")

		name = self.target_name or "Target date"
		pretty_date = self.target_date.strftime("%B %-d, %Y")
		self.date_label.set_text(f"{name} · {pretty_date}")

	def on_preferences(self, menuitem):
		self.event_entry.set_text(self.target_name)
		if self.target_date is not None:
			self.date_calendar.select_month(self.target_date.month - 1, self.target_date.year)
			self.date_calendar.select_day(self.target_date.day)

		response = self.prefs_dialog.run()

		if response == Gtk.ResponseType.OK:
			year, month, day = self.date_calendar.get_date()
			chosen = datetime.date(year, month + 1, day)
			self.settings.set_string("target-name", self.event_entry.get_text().strip())
			self.settings.set_string("target-date", chosen.isoformat())

		self.prefs_dialog.hide()

	def on_quit(self, menuitem):
		self.quit()

	def on_help(self, menuitem):
		self.about_dialog.run()
		self.about_dialog.hide()


if __name__ == "__main__":
	app = CountdownMachine()
	app.run(sys.argv)