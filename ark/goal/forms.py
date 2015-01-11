from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField
from wtforms import StringField, DateTimeField
from wtforms.validators import InputRequired, Length


class CreateGoalForm(Form):
    title = StringField(
        label=_(u'title'),
        validators=[
            InputRequired(),
            Length(min=1, max=100),
        ]
    )
    description = StringField(
        label=_(u'description'),
        validators=[
            InputRequired(),
            Length(min=5, max=200),
        ]
    )
    image = FileField(
        label=_('image'),
        validators=[
            InputRequired(),
        ]
    )


class GoalActivityForm(Form):
    activity = StringField(
        label=_('Activity'),
        validators=[
            InputRequired(),
            Length(min=5, max=200),
        ]
    )
    image = FileField(label=_('image'))
