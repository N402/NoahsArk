from flask.ext.wtf import Form
from flask.ext.html5 import EmailField
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo


EMAIL_RE = '(?:^[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+$)|(?:^$)'


class SignUpForm(Form):
    username = StringField(
        label=u'username',
        description=u'6-30 characters',
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    is_male = SelectField(
        label=u'gender',
        choices=[
            ('True', 'boy'),
            ('False', 'girl')
        ],
        validators=[InputRequired()]
    )
    email = EmailField(
        label=u'email',
        description=u'Your email address',
        validators=[
            InputRequired(message=u'please input your email'),
            Regexp(regex=EmailField, message=u'your email is invalid')]
    )
    password = PasswordField(
        label=u'password',
        description=u'6-30 characters',
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    confirm_password = PasswordField(
        label=u'confirm password',
        description=u'repeat your paassword',
        validators=[
            EqualTo('password')
        ])


class SignInForm(Form):
    email = EmailField(
        label=u'email',
        validators=[
            InputRequired(message=u'please input your email'),
            Regexp(regex=EmailField, message=u'your email is invalid')]
    )
    password = PasswordField(
        label=u'password',
        description=u'6-30 characters',
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ])
    remember_me = BooleanField(label=u'remember me')
