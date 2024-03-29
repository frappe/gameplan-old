# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.utils import get_fullname, now_datetime

def get_discussion_list(filters=None):
	if not filters:
		filters = {}

	if not 'published' in filters:
		filters['published'] = 1

	if not 'archived' in filters:
		filters['archived'] = 0

	discussions = frappe.get_all("Discussion",
		fields= ["page_name", "parent_website_route", "title", "owner", "name",
			"modified", "`read`"],
		filters= filters,
		order_by= "modified desc", limit_page_length=20)

	for d in discussions:
		d.timesince = timesince(d.modified, default="now", small=True)
		d.read = json.loads(d.read or "[]")
		if not frappe.session.user in d.read:
			d.unread = True

	return discussions


def update_discussion_user(doc, event):
	if doc.name != "Guest":
		current_username = frappe.db.get_value("User", doc.name, "username")

		if not frappe.db.exists("Discussion User", doc.username):
			frappe.get_doc({
				"doctype": "Discussion User",
				"name": doc.username
			}).insert(ignore_permissions=True)

		else:
			if current_username != doc.username:
				# username is changed!
				frappe.rename_doc("User", current_username, doc.username, ignore_permissions=True)

				# save it, since the route has changed
				discussion_user = frappe.get_doc("Discussion User", doc.username)
				discussion_user.save(ignore_permissions=True)


def get_user_info(user=None):
	if not hasattr(frappe.local, "user_info"):
		frappe.local.user_info = {}

	if not user:
		user = frappe.session.user

	if user not in frappe.local.user_info:
		username = frappe.db.get_value(
			"User", user, "username")

		color = frappe.db.get_value(
			"Discussion User", username, "color")

		frappe.local.user_info[user] = {
			"username": username,
			"color": color,
			"fullname": get_fullname(user)
		}

	return frappe.local.user_info[user]

def timesince(dt, default="just now", small=False):
	"""
	Returns string representing "time since" e.g.
	3 days ago, 5 hours ago etc.
	"""
	now = now_datetime()
	print now, dt

	diff = now - dt

	periods = (
		(diff.days / 365, "year", "years"),
		(diff.days / 30, "month", "months"),
		(diff.days / 7, "week", "weeks"),
		(diff.days, "day", "days"),
		(diff.seconds / 3600, "hour", "hours"),
		(diff.seconds / 60, "minute", "minutes"),
		(diff.seconds, "second", "seconds"),
	)

	for period, singular, plural in periods:
		if period:
			if small:
				return "%d %s" % (period, singular[0])
			else:
				return "%d %s ago" % (period, singular if period == 1 else plural)

	return default

def get_home_page(user):
	if user=='Guest':
		return 'login'
	else:
		return 'index'
