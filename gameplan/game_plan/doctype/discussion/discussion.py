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

    def get_email(self, username):
        return frappe.db.get_value(
            "User", username, "username")

    def get_context(self, context):
        usernames = {}
        user_colors = {}
        for comment in context.comments:
            if not comment.user in usernames:
                usernames[comment.user] = frappe.db.get_value(
                    "User", comment.user, "username")
                user_colors[comment.user] = frappe.db.get_value(
                    "Discussion User", self.get_email(comment.user), "color")
                print(user_colors)
            comment.username = usernames[comment.user]
            comment.user_color = user_colors[comment.user]

        context.owner_username = self.get_email(context.owner)
        context.owner_color = frappe.db.get_value(
            "Discussion User", context.owner_username, "color")

    def validate(self):
        super(Discussion, self).validate()
        self.parent_website_route = frappe.db.get_value("User", self.owner,
                                                        "username")

        if self.archived and not self.page_name.endswith("-archived"):
            self.page_name = self.page_name + "-archived"
