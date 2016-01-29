# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json

from frappe.utils.file_manager import save_file
from gameplan.utils import get_user_info, get_discussion_list
from frappe import _

@frappe.whitelist()
def new_discussion(title, content, files):
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

	save_files(files, discussion.doctype, discussion.name)

	frappe.publish_realtime("discussion_list_update")

	return discussion.get_route()

@frappe.whitelist()
def add_comment(name, content, files):
	discussion = frappe.get_doc("Discussion", name)
	discussion.append("comments", {"content": content, "user": frappe.session.user})
	discussion.read = None
	discussion.save(ignore_permissions=True)


	last_comment = discussion.comments[-1]

	save_files(files, last_comment.doctype, last_comment.name)

	last_comment.update(get_user_info(last_comment.user))
	last_comment.attachments = discussion.get_attachments(last_comment.doctype, last_comment.name)

	frappe.publish_realtime("new_comment", {
		"discussion_name": discussion.name,
		"comment_html": frappe.get_template("gameplan/templates/includes/new_comment.html")\
			.render({"comment": last_comment })
	})
	frappe.publish_realtime("discussion_list_update", {})

	return "ok"


def save_files(files, doctype, name):
	if files:
		files = json.loads(files)
		for file in files:
			save_file(file['name'], file['content'], doctype, name,
				decode=True, is_private=1)

@frappe.whitelist()
def delete_discussion(name):
	discussion = frappe.get_doc("Discussion", name)
	if discussion.owner == frappe.session.user:
		discussion.archive()

		frappe.publish_realtime("discussion_list_update", {})

	else:
		frappe.throw(_("Not Permitted"))

@frappe.whitelist()
def refresh_discussion_list():
	return frappe.get_template("gameplan/templates/includes/discussion_list.html")\
		.render({ "discussions": get_discussion_list() })
