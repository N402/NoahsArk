#-*- coding: utf-8
import time
from datetime import datetime


def format_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%Y-%m-%d')


def friendly_time(time):
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
    elif day_diff < 31:
        return u'%s 周前' % str(day_diff / 7)
    elif day_diff < 365:
        return u'%s 月前' % str(day_diff / 30)
    return u'%s 年前' % (day_diff / 365)
