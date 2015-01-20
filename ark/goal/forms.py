from flask.ext.wtf import Form
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
    image_name = StringField(_('Image Name'))
    image_url = StringField(_('Image URL'), validators=[InputRequired()])


class GoalActivityForm(Form):
    activity = TextAreaField(
        label=_('Activity'),
        validators=[
            InputRequired(),
            Length(min=5, max=200),
        ]
    )
    image_name = StringField(_('Image Name'))
    image_url = StringField(label=_('image'))
