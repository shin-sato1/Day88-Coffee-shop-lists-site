from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,PasswordField
from wtforms.validators import DataRequired,URL,InputRequired,Email

class AddForm(FlaskForm):
    cafe_name = StringField('Cafe name',validators=[DataRequired()])
    location = StringField('Cafe Location',validators=[DataRequired()])
    seats =  StringField('Seat',validators=[DataRequired()])
    coffee_price = StringField('Cafe Price',validators=[DataRequired()])
    map_url = StringField('Cafe Map URL',validators=[DataRequired(),URL()])
    img_url = StringField('Cafe Image URL',validators=[DataRequired(),URL()])
    sockets = SelectField('Socket Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    toilets =  SelectField('Toilet Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    wifis =  SelectField('Wi-fi Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    calls =  SelectField('Call Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = StringField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('submit')


