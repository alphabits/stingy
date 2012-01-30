import random
import string

from werkzeug.datastructures import MultiDict


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

def data_to_formdata(data, prefix=''):
    formdata = []

    iterator = enumerate(data) if type(data) == list else data.iteritems()

    for k, v in iterator:
        newprefix = prefix + str(k)

        if type(v) in [list, dict]:
            formdata.extend(data_to_formdata(v, prefix=newprefix+'-'))
        else:
            formdata.append((newprefix, str(v)))

    return formdata

def data_to_multidict(data):
    return MultiDict(data_to_formdata(data))
