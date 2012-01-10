import random
import string


def get_random_string(length=16, chars=string.ascii_lowercase+string.digits):
    return ''.join([random.choice(chars) for x in range(length)])

def group(s):
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + '.'.join(reversed(groups))

def money_format(value):
    if value is None:
        return ''
    string = '{0:.2f}'.format(value)
    integer, decimal = string.split('.')
    return group(integer) + ',' + decimal
