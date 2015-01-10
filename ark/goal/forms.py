from flask.ext.wtf import Form
from wtforms import StringField, TextField, DateTimeField


class CreateGoalForm(Form):
    title = StringField(
        label=_(u'title'),
        validators=[
            InputRequired(),
        ]
    )
    content = TextField(
        label=_(u'content'),
        validators=[
            InputRequired(),
        ]
    )
    start_at = DateTimeField(label=_(u'start at'))
    end_at = DateTimeField(label=_(u'end at'))
