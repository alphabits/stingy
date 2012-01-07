import random
import string


def get_random_string(length=16, chars=string.ascii_lowercase+string.digits):
    return ''.join([random.choice(chars) for x in range(length)])
