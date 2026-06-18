from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,URL,InputRequired

class Addform(FlaskForm):
    cafe_name = StringField('Cafe name',validators=[DataRequired()])
    location = StringField('Cafe Location',validators=[DataRequired()])
    coffee_price = StringField('Cafe Price',validators=[DataRequired()])
    map_url = StringField('Cafe Map URL',validators=[DataRequired(),URL()])
    img_url = StringField('Cafe Image URL',validators=[DataRequired(),URL()])
    sockets = SelectField('Socket Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    toilets =  SelectField('Toilet Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    wifis =  SelectField('Wi-fi Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    calls =  SelectField('Call Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    seats =  SelectField('Seat Y/N',validators=[InputRequired()],choices=[('True','Yes'),('False','No')])
    submit = SubmitField('Submit')

