# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

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


