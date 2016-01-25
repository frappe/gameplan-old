from __future__ import unicode_literals
import frappe

from gameplan.utils import timesince

def get_context(context):
	context.discussions = frappe.get_all("Discussion",
		fields=["page_name", "parent_website_route", "title", "owner", "name",
			"modified"],
		filters={"published": 1},
		order_by="modified desc", limit_page_length=20)

	for d in context.discussions:
		d.timesince = timesince(d.modified, default="now", small=True)
