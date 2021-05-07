from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, InputRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=36)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=36)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    task = StringField('Create a new task', validators=[DataRequired(), Length(min=1, max=50)])
    priority = SelectField(u'Priority', choices=[("1", "High"), ("2", "Medium"), ("3", "Low")] , validators=[InputRequired()])
    submit = SubmitField('Submit')

class TaskComment(FlaskForm):
    comment = StringField('Leave a comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Comment')

class ProjectForm(FlaskForm):
    project = StringField('Create a new project', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Submit')

class InviteForm(FlaskForm):
    username = StringField('Invite a new user to this project', validators=[DataRequired(), Length(min=3, max=36)])
    submit = SubmitField('Invite')