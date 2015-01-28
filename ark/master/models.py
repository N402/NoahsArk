from ark.exts import db


class SystemSetting(db.Model):

    __tablename__ = 'system_setting'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32))
    value = db.Column(db.Text())
