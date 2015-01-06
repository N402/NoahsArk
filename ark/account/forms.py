from flask.ext.wtf import Form
from flask.ext.html5 import EmailField
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask.ext.babel import lazy_gettext as _


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
