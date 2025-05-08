from flask import jsonify, request, send_file, render_template
from app.forms import *
from app import db
from app.models import *
from flask_login import current_user

import matplotlib.pyplot as plt
import io
import numpy as np

ENDPOINT = "budget"

def budget_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", "budget_api", budget_api, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/pie_chart", "budget_pie_chart", pie_chart, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/goals", "budget_goals", goals, methods=["GET"])
    
    # Add your friend's routes that work
    app.add_url_rule(
        f"{prefix}/{ENDPOINT}/get-budget-data",
        "get_budget_data",
        get_budget_data,
        methods=["GET"]
    )
    
    app.add_url_rule(
        f"{prefix}/{ENDPOINT}/update-budget-data",
        "update_budget_data",
        update_budget_data,
        methods=["POST"]
    )

def budget_api():
    return jsonify({"status": "budget"}), 200

def graph_error(message):
    plt.figure(figsize=(6, 4)) 
    plt.axis('off')

    plt.title('Could Not Generate Graph', fontsize=20)
    plt.text(0.5, 0.5, f"{message}", fontsize=16, ha='center', va='center')

    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

def pie_chart():
    if request.method != "GET":
        return jsonify({"status":"error","message":"Method not allowed."}), 405

    try:
        try:
            userid = current_user.id
        except:
            return graph_error("Could not Retrieve User Data")
        
        financials = Financials.query.filter_by(userid=userid).first()

        if not financials:
            return graph_error("Budget not set")
        
        # Get budget categories and values
        categories = ["food", "rent", "utilities", "shopping", "entertainment", "other"]
        values = []
        labels = []
        
        for category in categories:
            budget_value = getattr(financials, category, 0)
            if budget_value and float(budget_value) > 0:
                values.append(float(budget_value))
                labels.append(category.capitalize())
        
        if not labels or not values:
            return graph_error("No budget categories with values")
        
        # Create a pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
                colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'])
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Budget Allocation')
        
        # Save the chart to a bytes buffer
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        return send_file(img, mimetype='image/png')
    
    except Exception as e:
        return graph_error(f"Exception: {e}")

def goals():
    if request.method != "GET":
        return jsonify({"status":"error","message":"Method not allowed."}), 405
    
    try:
        userid = current_user.id
        financials = Financials.query.filter_by(userid=userid).first()
        
        if not financials:
            return jsonify({"status": "error", "message": "Budget not set"}), 400
        
        # Get saving goals (assuming goal1, goal2, goal3 are the saved amounts)
        goals_data = []
        
        # Target amount for goals - in a real app you'd have this saved somewhere
        target_amount = 100  # Default target
        
        for i in range(1, 4):
            goal_attr = f"goal{i}"
            goal_amount = getattr(financials, goal_attr, 0)
            
            if goal_amount is not None:
                goal_amount = float(goal_amount)
                progress = min(100, int((goal_amount / target_amount) * 100))
                
                goals_data.append({
                    "id": i,
                    "current": goal_amount,
                    "target": target_amount,
                    "progress": progress
                })
        
        return jsonify({
            "status": "success", 
            "goals": goals_data,
            "currency": financials.currency
        }), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Exception: {str(e)}"}), 500

# Add the functions from your friend's code that work
def get_budget_data():
    """
    API endpoint to get budget data
    This uses the get_inc_budget function from data.py
    """
    from app.api.data import get_inc_budget
    try:
        return get_inc_budget()
    except Exception as e:
        return jsonify({"status":"error", "message": str(e)}), 500

def update_budget_data():
    """
    API endpoint to update budget data
    This uses the set_inc_budget function from data.py
    """
    from app.api.data import set_inc_budget
    try:
        return set_inc_budget()
    except Exception as e:
        return jsonify({"status":"error", "message": str(e)}), 500