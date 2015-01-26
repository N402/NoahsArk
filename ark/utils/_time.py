#-*- coding: utf-8
import time
from datetime import datetime

from flask.ext.babel import format_datetime


def friendly_time(time, fallback_format=None):
    now = datetime.utcnow()
    if type(time) is datetime:
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''
    elif day_diff == 0:
        if second_diff < 10:
            return u'刚刚'
        elif second_diff < 60:
            return u'%s 秒前' % str(second_diff)
        elif second_diff < 120:
            return u'1 分钟前'
        elif second_diff < 3600:
            return u'%s 分钟前' % str(second_diff / 60)
        elif second_diff < 7200:
            return u'1 小时前'
        elif second_diff < 86400:
            return u'%s 小时前' % str(second_diff / 3600)
    elif day_diff == 1:
        return u'昨天'
    elif day_diff < 7:
        return u'%s 天前' % str(day_diff)
    return format_datetime(time, fallback_format)
