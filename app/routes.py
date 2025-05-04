from app import app
from app.forms import *
from flask import render_template , flash
from flask_login import current_user, login_user
from app.models import User 


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    sf = settingsform()
    return render_template('profile.html', form=sf)

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/projections')
def projections():
    analysis = {
        'total_projects': 10,
        'completed_projects': 7,
        'completion_rate': 70
    }

    projects = [
        {'id': 1, 'name': 'Project Alpha', 'status': 'Completed', 'progress': 100},
        {'id': 2, 'name': 'Project Beta', 'status': 'Ongoing', 'progress': 60},
        # add more if needed
    ]

    return render_template('projections.html', analysis=analysis, projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if current_user.is_authenticated: 
        return redirect(url_for('data')) 
    form = LoginForm() 
    return render_template('login.html', title='Sign In', form=form)
 



