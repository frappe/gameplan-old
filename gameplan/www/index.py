from __future__ import unicode_literals
import frappe

def get_context(context):
	context.discussions = frappe.get_all("Discussion",
		fields=["page_name", "parent_website_route", "title"],
		filters={"published": 1},
		order_by="creation desc", limit_page_length=20)
