import re

from utils import eventutil


def validate_iso8601(iso_string):
    """Validate whether or not a string meets the ISO8601 date format."""
    return re.search(
        '^([0-9]{4})(-)?(1[0-2]|0[1-9])(?(2)-)(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9])(?(2):)([0-5][0-9])(?(2):)([0-5][0-9])$',
        iso_string)


def validate_post_body(attributes):
    """Validate the post body attributes. Passed in order of code, name, start, end, and desc."""
    if not attributes['api_key']:
        return False
    elif attributes['eventcode'] is None:
        attributes['eventcode'] = eventutil.gen_code()
    elif attributes['eventname'] is None:
        return False
    elif not (validate_iso8601(attributes['starttime']) and validate_iso8601(attributes['endtime'])):
        return False

    return True
