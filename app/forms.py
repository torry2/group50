from flask import Flask, render_template, request, redirect, url_for 
from flask_wtf import FlaskForm 
from wtforms import StringField, validators, PasswordField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, NumberRange, InputRequired
from decimal import Decimal

class settingsform(FlaskForm):
    new_password = PasswordField('Change Password', validators=[DataRequired()])
    currency = SelectField('Select Currency', choices=[('AUD', 'AUD'), ('USD', 'USD')], validators=[DataRequired()])
    save = SubmitField('Save')

class deleteForm(FlaskForm):
    delete = SubmitField('Delete Account')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class TransactionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Rent', 'Rent'), ('Utilities', 'Utilities'), ('Shopping', 'Shopping'), ('Entertainment', 'Entertainment'), ('Other', 'Other'), ('Goal 1', 'Goal 1'), ('Goal 2', 'Goal 2'), ('Goal 3', 'Goal 3')], validators=[DataRequired()])
    amount = DecimalField('Amount', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    submit = SubmitField('Add')

class ProjectionsForm(FlaskForm):
    submit = SubmitField('Analyse')

class IncomeBudgetForm(FlaskForm):
    income = DecimalField('Income', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    food_budget = DecimalField('Food', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    rent_budget = DecimalField('Rent', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    utilities_budget = DecimalField('Utilities', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    shopping_budget = DecimalField('Shopping', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    entertainment_budget = DecimalField('Entertainment', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    other_budget = DecimalField('Other', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    goal1_budget = DecimalField('Goal 1', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    goal2_budget = DecimalField('Goal 2', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    goal3_budget = DecimalField('Goal 3', places=2, rounding=None, validators=[InputRequired(), NumberRange(min=Decimal('0.00'))])
    submit = SubmitField('Save')