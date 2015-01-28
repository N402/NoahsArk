from flask.ext.babel import lazy_gettext as _

from ark.exts import db


class SystemSetting(db.Model):

    __tablename__ = 'system_setting'

    KEY_TYPES = {
        'msg_first_login': _('First Login Message'),
        'msg_rollcalled': _('Rollcalled Message'),
        'msg_failed': _('Failed Message'),
    }

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Enum(*(KEY_TYPES.keys())))
    value = db.Column(db.Text())

    def display_name(self):
        return self.KEY_TYPES[self.key]
