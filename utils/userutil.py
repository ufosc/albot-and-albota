from enum import Enum

from cogs import CONSTANTS


class Permission(Enum):
    """For all permissions: false for Admin ONLY, else all users have permission"""
    EVENT_CREATE = False,  # permission for creating new events (admin)
    EVENT_DESTROY = False,  # permission for destroying events (admin)
    EVENT_MODIFY = False,  # permission for modifying event details (admin)
    EVENT_SIGNIN = True,  # permission for signing into an event
    EVENT_LIST = True,  # permission for seeing a list of upcoming events and their dates
    EVENT_VIEW = True,  # permission for seeing details about a past, upcoming, or active event

    @staticmethod
    def get_user_descriptions(user):
        """Returns a string list of usable event permission for a user."""
        descs = '>>>'
        for permission, value in Permission.__members__.items():
            perm = Permission[permission]
            if has_permission(user, perm):
                descs += f'{Permission.get_desc(perm)}\n'

    @staticmethod
    def get_desc(permission):
        if permission == Permission.EVENT_CREATE:
            return '* event create <?:code> <name> <startdate> <enddate> Used for creating and scheduling new events on the site backend. Codes (optional) must be unique 6-digit [A-Z0-9] characters.\n\nTime formatting: **YYYY-MM-DDThh:mm:SS**'
        elif permission == Permission.EVENT_DESTROY:
            return '* event rm <code> - Used for destroying events.'
        elif permission == Permission.EVENT_MODIFY:
            return '* event modify <code> {values: \'here\'} - Used for modifying events.'
        elif permission == Permission.EVENT_SIGNIN:
            return '* event signin - Used for signing into an event.'
        elif permission == Permission.EVENT_LIST:
            return '* event list - Used for seeing a list of upcoming events and their dates.'
        elif permission == Permission.EVENT_VIEW:
            return '* event view <code> - Used for seeing event details.'


def is_officer(member):
    """Determine whether or not a member has the officer role."""
    return member.top_role.id == CONSTANTS.OFFICER_ROLE


def has_permission(member, permission: Permission):
    """Helper method to determine if user has a permission to perform event actions."""
    return is_officer(member) and permission.value
