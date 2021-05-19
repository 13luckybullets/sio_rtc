import random
import string
from datetime import datetime


def get_random_str(num=4):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(num))


def now():
    return datetime.now().strftime('%H_%M_%S')


def get_rand_name():
    name = now()
    key = get_random_str()
    return f"{name}_{key}"

