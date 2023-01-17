from flask_wtf import FlaskForm
from wtforms import Form, TextAreaField, StringField, SelectField, SubmitField, PasswordField, validators



class TodoForm(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired(), validators.Length(min=4, max=25)])
    description = TextAreaField("Description", validators=[validators.DataRequired()])
    completed = SelectField("Completed", choices=[("True", "True"), ("False", "False")], validators=[validators.DataRequired()])
    submit = SubmitField("Add Todo")

