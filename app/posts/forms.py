from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired(), Length(max=60)])
    content = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Add Post')
