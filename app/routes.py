from app.forms import *
from flask import render_template, flash, redirect, url_for, send_file, request, jsonify
from flask_login import current_user, login_required
from app.models import User
from app import login
from app.api.data import data_routes
from app.api.budget import budget_routes, goals, pie_chart
from app.api.minimal_share import share_routes
from app.blueprints import main

API_PREFIX = "/api"

@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('main.login'))

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/profile')
@login_required
def profile():
    sf = settingsform()
    return render_template('profile.html', form=sf)

@main.route('/budget', methods=['GET', 'HEAD'])
@login_required
def budget():
    return render_template('budget.html')

@main.route('/data', methods=['GET', 'POST', 'DELETE'])
@login_required
def data():
    transaction_form = TransactionForm()
    inc_budget_form = IncomeBudgetForm()
    return render_template('data.html', transaction_form=transaction_form, inc_budget_form=inc_budget_form)

@main.route('/projections')
@login_required
def projections():
    pf = ProjectionsForm()
    return render_template('projections.html', form=pf)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.data'))
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@main.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    if request.method == 'GET':
        goal_id = request.args.get('goal')
        return render_template('share.html', goal_id=goal_id)
        
            