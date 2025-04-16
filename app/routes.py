from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('default.html')  # assuming this is inside templates

@main.route('/budget')
def budget():
    return render_template('budget.html')


