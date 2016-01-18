# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

class DiscussionUser(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/user.html",
		condition_field = "published",
		page_title_field = "username",
		no_cache = True
	)

	def validate(self):
		super(DiscussionUser, self).validate()
		self.parent_website_route = ''
		self.page_name = self.name

	def get_context(self, context):
		context.discussions = frappe.get_all("Discussion",
			fields=["page_name", "parent_website_route", "title"],
			filters={"published": 1, "owner": frappe.session.user},
			order_by="creation desc", limit_page_length=20)
