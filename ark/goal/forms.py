from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import InputRequired, Length
from flask.ext.babel import lazy_gettext as _


class CreateGoalForm(Form):
    title = StringField(
        label=_(u'title'),
        validators=[
            InputRequired(),
            Length(min=1, max=100),
        ]
    )
    description = TextAreaField(
        label=_(u'description'),
        validators=[
            InputRequired(),
            Length(min=5, max=200),
        ]
    )
    image = FileField(_('image'), validators=[FileRequired()])


class GoalActivityForm(Form):
    activity = StringField(
        label=_('Activity'),
        validators=[
            InputRequired(),
            Length(min=5, max=200),
        ]
    )
    image = FileField(label=_('image'))
