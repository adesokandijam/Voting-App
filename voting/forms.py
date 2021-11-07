from operator import pos
from flask.app import Flask
from flask_wtf import FlaskForm, validators
from wtforms import StringField, SubmitField, PasswordField, RadioField
import wtforms
from wtforms.fields.core import FormField, Label, SelectField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from voting.models import Candidate, Position, User

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email_address = StringField(label="Email-Address",validators=[DataRequired()])
    department = StringField(label="Department", validators=[DataRequired()])
    password1 = PasswordField(label="Enter Password",validators=[DataRequired()])
    password2 = PasswordField(label="Confirm your Password", validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label="Submit")

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email address already exist! Please try a different username')

class LoginForm(FlaskForm):
    email_address = StringField(label="Email-Address",validators=[DataRequired()])
    password = PasswordField(label="Enter Password",validators=[DataRequired()])
    submit = SubmitField(label="Log In")

class PresidentForm(FlaskForm):
    example = SelectField(label = "President", choices=Candidate.query.filter_by(position = "President").all())

class VicePresidentForm(FlaskForm):
    example = SelectField(label = "Vice President", choices=Candidate.query.filter_by(position = "Vice President").all())


class SecretaryForm(FlaskForm):
    example = SelectField(label = "Secretary", choices=Candidate.query.filter_by(position = "Secretary").all())


class TreasurerForm(FlaskForm):
    example = SelectField(label = "Treasurer", choices=Candidate.query.filter_by(position = "Treasurer").all())


class AGSForm(FlaskForm):
    example = SelectField(label = "Assistant General Secratary", choices=Candidate.query.filter_by(position = "AGS").all())


class SportsDirectorForm(FlaskForm):
    example = SelectField(label = "Sports Director", choices=Candidate.query.filter_by(position = "Sports Director").all())


    
class CandidateForm(FlaskForm):
    name = StringField(label="Username", validators=[DataRequired()])
    department = StringField(label="Department", validators=[DataRequired()])
    position = SelectField(label="Select Position", choices=Position.query.all())
    submit = SubmitField(label="Submit")

class GiantForm(FlaskForm):
    president = FormField(PresidentForm)
    vice_president = FormField(VicePresidentForm)
    secretary = FormField(SecretaryForm)
    ags = FormField(AGSForm)
    treasurer = FormField(TreasurerForm)
    sports_director = FormField(SportsDirectorForm)
    submit = SubmitField(label="Submit")


