from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from flask.ext.login import current_user
from wtforms import (
    StringField, PasswordField, BooleanField, SelectField, TextAreaField)
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms.validators import ValidationError
from flask.ext.babel import lazy_gettext as _

from ark.account.models import Account


class SignUpForm(Form):
    username = StringField(
        label=_(u'Username'),
        validators=[
            InputRequired(),
            Length(min=4, max=30),
        ])
    email = EmailField(
        label=_(u'Email'),
        validators=[
            InputRequired(message=_(u'please input your email')),
            Email(message=_(u'your email is invalid'))]
    )
    password = PasswordField(
        label=_(u'Password'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
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
    signin_email = EmailField(
        label=_(u'email'),
        validators=[
            InputRequired(message=_(u'please input your email')),
            Email(message=_(u'your email is invalid'))]
    )
    signin_password = PasswordField(
        label=_(u'password'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    remember_me = BooleanField(label=_(u'remember me'))


class ProfileForm(Form):
    email = EmailField(
        label=_(u'Email'),
        validators=[
            Email(message=_(u'Your Email is invalid'))])
    username = StringField(
        label=_(u'username'),
        validators=[
            InputRequired(),
            Length(min=4, max=30),
        ])
    whatsup = TextAreaField(
        label=_('whatsup'),
    )

    def validate_email(form, field):
        query_user = Account.query.filter(Account.email==field.data)
        if query_user.count() > 0 and query_user.id != current_user.id:
            raise ValidationError(_(u'Email exists'))

    def validate_username(form, field):
        query_user = Account.query.filter(Account.username==field.data)
        if query_user.count() > 0 and query_user.id != current_user.id:
            raise ValidationError(_(u'Username exists'))


class AvatarForm(Form):
    avatar_url = StringField(
        label=_('avatar'),
        validators=[InputRequired(),],)


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
            EqualTo('new_password', message=_('Confirm password not match'))
        ])

    def validate_old_password(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError(_(u'old password is wrong'))
