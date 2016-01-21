# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappé and March and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator


class Discussion(WebsiteGenerator):
    website = frappe._dict(
        template="templates/generators/discussion.html",
        condition_field="published",
        page_title_field="title",
        no_cache=True
    )

    def get_context(self, context):
        usernames = {}
        for comment in context.comments:
            if not comment.user in usernames:
                usernames[comment.user] = frappe.db.get_value(
                    "User", comment.user, "username")
            comment.username = usernames[comment.user]

        owner_username = frappe.db.get_value(
            "User", context.owner, "username")
        context.owner_color = frappe.db.get_value(
            "Discussion User", owner_username, "color")

    def validate(self):
        super(Discussion, self).validate()
        self.parent_website_route = frappe.db.get_value("User", self.owner,
                                                        "username")

        if self.archived and not self.page_name.endswith("-archived"):
            self.page_name = self.page_name + "-archived"
