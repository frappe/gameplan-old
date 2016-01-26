# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
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

		context.doc.update(get_user_info(context.owner))

		context.user_info = get_user_info(frappe.session.user)

		# update read
		context.read = json.loads(self.read or "[]")
		if not frappe.session.user in context.read:
			context.read.append(frappe.session.user)
			self.db_set("read", json.dumps(context.read), update_modified=False)
			frappe.db.commit()


	def before_insert(self):
		self.read = json.dumps([frappe.session.user])

	def validate(self):
		super(Discussion, self).validate()
		self.parent_website_route = frappe.db.get_value("User", self.owner,
			"username")

		if self.archived and not self.page_name.endswith("-archived"):
			self.page_name = self.page_name + "-archived"

		if not self.read:
			self.read = json.dumps([self.comments[-1].user])
