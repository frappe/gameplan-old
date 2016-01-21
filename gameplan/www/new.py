from __future__ import unicode_literals
import frappe


def get_context(context):
    context.username = frappe.db.get_value(
        "User", frappe.session.user, "username")

    context.user_color = frappe.db.get_value(
        "Discussion User", context.username, "color")
