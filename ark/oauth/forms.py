from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import ValidationError, InputRequired, Length
from flask.ext.babel import lazy_gettext as _

from ark.account.models import Account


class OAuthSignUpForm(Form):
    username = StringField(
        label=_('Username'),
        validators=[
            InputRequired(),
            Length(min=4, max=30),
        ])

    def validate_username(form, field):
        query_user = Account.query.filter(Account.username==field.data)
        if query_user.count() > 0:
            raise ValidationError(_(u'Username %(username)s exists', username=field.data))
