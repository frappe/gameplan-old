from __future__ import unicode_literals
import gameplan.utils
import frappe

def get_context(context):
	filters = {}
	if frappe.form_dict.q:
		filters = {
			"title": ("like", "%{0}%".format(frappe.form_dict.q)),
			"archived": ("in", ("0", "1"))
		}
	context.discussions = gameplan.utils.get_discussion_list(filters)
