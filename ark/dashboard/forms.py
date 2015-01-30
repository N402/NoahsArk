from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from flask.ext.babel import lazy_gettext as _

from ark.account.models import Account


class AccountEditForm(Form):

    username = StringField(_(u'Username'),
                           validators=[InputRequired(),
                                       Length(min=3, max=30)])
    gender = SelectField(_(u'Gender'),
                          choices=[
                              ('male', _('Male')),
                              ('female', _('Female')),])
    password = PasswordField(_('Password'),)
    state = SelectField(_('State'),
                        choices=(('normal', _('Normal')),
                                 ('frozen', _('Frozen')),
                                 ('deleted', _('Deleted')),
                                 ('inactive', _('Inactive')),))
    is_superuser = SelectField(_('Superuser'),
                               choices=[
                                   ('True', _('Yes')),
                                   ('False', _('No'))])


class GoalEditForm(Form):
    is_deleted = SelectField(_('Is Deleted'),
                             choices=(('True', _('Yes')),
                                      ('False', _('No'))))


class GoalActivityEditForm(Form):
    is_deleted = SelectField(_('Is Deleted'),
                             choices=(('True', _('Yes')),
                                      ('False', _('No'))))


class NotificationSendForm(Form):
    content = TextAreaField(label=_('Content'), validators=[InputRequired()])
    receivers = QuerySelectMultipleField(
        label=_('Receivers'),
        query_factory=lambda: Account.query.filter(Account.state!='deleted').all(),
        get_label=lambda x: x.username,
    )


class SystemMsgForm(Form):
    msg_first_login = TextAreaField(label=_('First Login Message'))
    msg_rollcalled = TextAreaField(label=_('Rollcalled Message'))
    msg_failed = TextAreaField(label=_('Failed Message'))
