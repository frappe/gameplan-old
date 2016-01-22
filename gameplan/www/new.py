from __future__ import unicode_literals

from gameplan.utils import get_user_info

def get_context(context):
	context.user_info = get_user_info()
