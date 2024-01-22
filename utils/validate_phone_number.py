import re


def validate_phone_number(phone_number):
    if not len(phone_number) == 11:
        return False

    phone_rule = re.compile(r'^010[0-9]{8}$')

    if phone_rule.match(phone_number):
        return True
    else:
        return False