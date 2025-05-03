from flask import Flask, render_template, request, redirect, url_for 
from flask_wtf import FlaskForm 
from wtforms import StringField, validators, PasswordField, SelectField, SubmitField 
from wtforms.validators import DataRequired, Email 

class settingsform(FlaskForm):
    new_password = PasswordField('Change Password', validators=[DataRequired()])
    currency = SelectField('Select Currency', choices=[('AUD', 'AUD'), ('USD', 'USD')], validators=[DataRequired()])
    save = SubmitField('Save')
    delete = SubmitField('Delete Account')