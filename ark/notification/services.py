from ark.exts import db
from ark.master.models import SystemSetting
from ark.notification.models import Notification


def send_sysmsg(receivers, msg_content):
    sysmsg = Notification(content=msg_content)
    sysmsg.receivers = receivers
    db.session.add(sysmsg)
    db.session.commit()
    return True


def send_sysmsg_by_key(receivers, key):
    if not isinstance(receivers, (list,)):
        receivers = [receivers]
    sysmsg = SystemSetting.query.filter(SystemSetting.key==key).first()
    if sysmsg:
        return send_sysmsg(receivers, sysmsg.value)
    else:
        return False


def send_first_login_sysmsg(receivers):
    return send_sysmsg_by_key(receivers, 'msg_first_login')


def send_rollcalled_sysmsg(receivers):
    return send_sysmsg_by_key(receivers, 'msg_rollcalled')


def send_msg_failed_sysmsg(receivers):
    return send_sysmsg_by_key(receivers, 'msg_failed')
