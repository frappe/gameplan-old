# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from gameplan.utils import get_user_info

@frappe.whitelist()
def new_discussion(title, content):
	discussion = frappe.new_doc("Discussion")
	discussion.title = title

	page_name = discussion.get_page_name()
	existing = frappe.db.get_value("Discussion", {"page_name": page_name}, "name")

	if existing:
		discussion = frappe.get_doc("Discussion", existing)
		discussion.append("comments", {"content": content, "user": frappe.session.user})
		discussion.save(ignore_permissions=True)

	else:
		discussion.content = content
		discussion.insert(ignore_permissions=True)

	return discussion.get_route()

@frappe.whitelist()
def add_comment(name, content):
	discussion = frappe.get_doc("Discussion", name)
	discussion.append("comments", {"content": content, "user": frappe.session.user})
	discussion.save(ignore_permissions=True)

	last_comment = discussion.comments[-1]
	last_comment.update(get_user_info(last_comment.user))

	return frappe.get_template("gameplan/templates/includes/new_comment.html")\
		.render({"comment": last_comment })


