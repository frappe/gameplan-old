# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import random_string
from frappe.website.website_generator import WebsiteGenerator
from gameplan.utils import get_user_info
import json

class Discussion(WebsiteGenerator):
	website = frappe._dict(
		template="templates/generators/discussion.html",
		condition_field="published",
		page_title_field="title",
		no_cache=True
	)

	def get_email(self, username):
		return frappe.db.get_value(
			"User", username, "username")

	def get_context(self, context):
		for comment in context.comments:
			comment.update(get_user_info(comment.user))
			comment.attachments = self.get_attachments(comment.doctype, comment.name)

		context.doc.update(get_user_info(context.owner))
		context.doc.attachments = self.get_attachments(self.doctype, self.name)

		context.user_info = get_user_info(frappe.session.user)

		# update read
		context.read = json.loads(self.read or "[]")
		if not frappe.session.user in context.read:
			context.read.append(frappe.session.user)
			self.db_set("read", json.dumps(context.read), update_modified=False)
			frappe.db.commit()

	def get_attachments(self, doctype, name):
		return [f.file_url for f in frappe.get_all("File",
			fields = ["file_url"],
			filters = {"attached_to_doctype": doctype, "attached_to_name": name})]

	def before_insert(self):
		self.read = json.dumps([frappe.session.user])

	def validate(self):
		super(Discussion, self).validate()
		self.parent_website_route = frappe.db.get_value("User", self.owner,
			"username")

		if not self.read:
			self.read = json.dumps([self.comments[-1].user])

	def archive(self):
		self.archived = 1
		self.page_name = self.page_name + '-' + random_string(10)
		self.title = "Archived: " + self.title
		self.save(ignore_permissions=True)
