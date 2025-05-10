from app import app
from app.forms import *
from flask import render_template, flash, redirect, url_for, send_file, request, jsonify
from flask_login import current_user, login_required
from app.models import User
from app import login
from app.api.data import data_routes
from app.api.budget import budget_routes, goals, pie_chart
from app.api.minimal_share import share_routes

API_PREFIX = "/api"
data_routes(app, API_PREFIX)  # transaction endpoints
budget_routes(app, API_PREFIX)  # budget endpoints
share_routes(app, API_PREFIX)  # share endpoints

@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
@login_required
def profile():
    sf = settingsform()
    return render_template('profile.html', form=sf)

@app.route('/budget', methods=['GET', 'HEAD'])
@login_required
def budget():
    return render_template('budget.html')

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
@login_required
def data():
    transaction_form = TransactionForm()
    inc_budget_form = IncomeBudgetForm()
    return render_template('data.html', transaction_form=transaction_form, inc_budget_form=inc_budget_form)

@app.route('/projections')
@login_required
def projections():
    pf = ProjectionsForm()
    return render_template('projections.html', form=pf)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('data'))
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/share', methods=['GET', 'POST'])
@login_required
def share():
        
    if request.method == 'GET':
        goal_id = request.args.get('goal')
        return render_template('share.html', goal_id=goal_id)
        
            