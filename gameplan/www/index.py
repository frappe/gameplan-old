from __future__ import unicode_literals
import frappe
import json

from gameplan.utils import timesince

def get_context(context):
	context.discussions = frappe.get_all("Discussion",
		fields=["page_name", "parent_website_route", "title", "owner", "name",
			"modified", "`read`"],
		filters={"published": 1},
		order_by="modified desc", limit_page_length=20)

	for d in context.discussions:
		d.timesince = timesince(d.modified, default="now", small=True)
		d.read = json.loads(d.read or "[]")
		if not frappe.session.user in d.read:
			d.unread = True
