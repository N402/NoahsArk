from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from flask.ext.login import current_user
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp
from wtforms.validators import ValidationError
from flask.ext.babel import lazy_gettext as _

from ark.account.models import Account


EMAIL_RE = '(?:^[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+$)|(?:^$)'


class SignUpForm(Form):
    username = StringField(
        label=_(u'username'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    is_male = SelectField(
        label=_(u'gender'),
        choices=[
            ('True', _('boy')),
            ('False', _('girl'))
        ],
        validators=[InputRequired()]
    )
    email = EmailField(
        label=_(u'email'),
        validators=[
            InputRequired(message=_(u'please input your email')),
            Regexp(regex=EmailField, message=_(u'your email is invalid'))]
    )
    password = PasswordField(
        label=_(u'password'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    confirm_password = PasswordField(
        label=_(u'confirm password'),
        validators=[
            EqualTo('password')
        ])

    def validate_email(form, field):
        query_user = Account.query.filter(Account.email==field.data)
        if query_user.count() > 0:
            raise ValidationError(_(u'Email exists'))

    def validate_username(form, field):
        query_user = Account.query.filter(Account.username==field.data)
        if query_user.count() > 0:
            raise ValidationError(_(u'Username exists'))

class SignInForm(Form):
    email = EmailField(
        label=_(u'email'),
        validators=[
            InputRequired(message=_(u'please input your email')),
            Regexp(regex=EmailField, message=_(u'your email is invalid'))]
    )
    password = PasswordField(
        label=_(u'password'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    remember_me = BooleanField(label=_(u'remember me'))


class SettingForm(Form):
    username = StringField(
        label=_(u'username'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])


class ChangePassword(Form):
    old_password = PasswordField(
        label=_(u'old password'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ],
    )
    new_password = PasswordField(
        label=_(u'new password'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    confirm_password = PasswordField(
        label=_(u'confirm password'),
        validators=[
            EqualTo('new_password')
        ])

    def validate_old_password(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError(_(u'old password is wrong'))
