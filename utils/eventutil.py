import uuid


def gen_code():
    """Generates a universally unique secure random string ID"""
    random_string = uuid.uuid4().hex  # get a random string in UUID format
    return random_string.upper()[0:6]
