#Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, EqualTo, Email

#Forms
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class CheckoutForm(FlaskForm):
    #Billing information
    firstname = StringField("First Name", validators=[InputRequired()])
    lastname = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired(), Length(min=2, max=20)])
    address = StringField("Address Line 1", validators=[InputRequired()])
    address2 = StringField("Address Line 2", validators=[InputRequired()])
    country = StringField("Country/Region", validators=[InputRequired()])
    city = StringField("Town/City", validators=[InputRequired()])
    postcode = StringField("Postcode", validators=[InputRequired(), Length(min=7, max=7)])
    #Payment information (not saved to database due to security issues)
    cardname = StringField("Name on Card", validators=[InputRequired()])
    cardno = StringField("Card Number", validators=[InputRequired(), Length(min=15, max=16)])
    cardexpire = DateField("Expiration", format='%m/%Y', validators=[InputRequired()])
    cvv = StringField("CVV", validators=[InputRequired(), Length(min=3, max=3)])
    submit = SubmitField("Place Order")

class PasswordForm(FlaskForm):
    currentPassword = PasswordField("Current password", validators=[InputRequired()])
    newPassword = PasswordField("New password", validators=[InputRequired()])
    checkNewPassword = PasswordField("Re-enter new password", validators=[InputRequired(), EqualTo("newPassword")])
    submit = SubmitField("Save Changes")
    