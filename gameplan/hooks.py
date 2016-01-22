# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "gameplan"
app_title = "Game Plan"
app_publisher = "Frappé and March"
app_description = "A Project Management Medium"
app_icon = "octicon octicon-rocket"
app_color = "grey"
app_email = "hello@frappe.io"
app_version = "0.0.1"
app_license = "No License"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gameplan/css/gameplan.css"
# app_include_js = "/assets/gameplan/js/gameplan.js"

# include js, css files in header of web template
web_include_css = "/assets/gameplan/css/style.css"
web_include_js = [
	"/assets/gameplan/js/jquery.textarea_autosize.min.js",
	"/assets/gameplan/js/gameplan.js"
]

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
website_generators = ["Discussion", "Discussion User"]

# Installation
# ------------

# before_install = "gameplan.install.before_install"
# after_install = "gameplan.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gameplan.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"validate": "gameplan.utils.update_discussion_user",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"gameplan.tasks.all"
# 	],
# 	"daily": [
# 		"gameplan.tasks.daily"
# 	],
# 	"hourly": [
# 		"gameplan.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gameplan.tasks.weekly"
# 	]
# 	"monthly": [
# 		"gameplan.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "gameplan.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gameplan.event.get_events"
# }

