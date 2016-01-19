# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

class Discussion(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/discussion.html",
		condition_field = "published",
		page_title_field = "title",
		no_cache = True
	)

	def validate(self):
		super(Discussion, self).validate()
		self.parent_website_route = frappe.db.get_value("User", self.owner,
			"username")

		if self.archived and not self.page_name.endswith("-archived"):
			self.page_name = self.page_name + "-archived"

