from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length
from flask.ext.babel import lazy_gettext as _


class EditAccountForm(Form):

    username = StringField(_(u'username'),
                           validators=[InputRequired(),
                                       Length(min=6, max=30)])
    gender = SelectField(_(u'gender'),
                          choices=[
                              ('male', _('male')),
                              ('female', _('female')),])
    password = PasswordField(_('password'),)
