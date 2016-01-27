from __future__ import unicode_literals
import gameplan.utils

def get_context(context):
	context.discussions = gameplan.utils.get_discussion_list()
