from flask import Flask, render_template, request, redirect, url_for 
from flask_wtf import FlaskForm 
from wtforms import StringField, validators, PasswordField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, NumberRange, InputRequired
from decimal import Decimal

class settingsform(FlaskForm):
    new_password = PasswordField('Change Password', validators=[DataRequired()])
    currency = SelectField('Select Currency', choices=[('AUD', 'AUD'), ('USD', 'USD')], validators=[DataRequired()])
    save = SubmitField('Save')
    delete = SubmitField('Delete Account')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class TransactionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Rent', 'Rent'), ('Utilities', 'Utilities'), ('Shopping', 'Shopping'), ('Entertainment', 'Entertainment'), ('Other', 'Other'), ('Goal1', 'Goal1'), ('Goal2', 'Goal2'), ('Goal3', 'Goal3')], validators=[DataRequired()])
    amount = DecimalField('Amount', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    submit = SubmitField('Add')

class ProjectionsForm(FlaskForm):
    submit = SubmitField('Get Projections')