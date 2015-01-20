from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length
from flask.ext.babel import lazy_gettext as _


class EditAccountForm(Form):

    username = StringField(_(u'Username'),
                           validators=[InputRequired(),
                                       Length(min=6, max=30)])
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
