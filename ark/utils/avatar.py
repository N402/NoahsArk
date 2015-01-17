from flask import url_for

from random import randint


def random_avatar():
    filename = "images/avatars/%s.png" % randint(0, 9)
    return url_for('static', filename=filename)
