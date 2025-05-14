from flask import jsonify, request, send_file
from app.forms import *
from app import db
from app.models import *
from flask_login import current_user

import matplotlib.pyplot as plt
import io

ENDPOINT = "projections"

def projections_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", "{prefix}/{ENDPOINT}", projections, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/graph", "graph", graph, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/habits", "habits", habits, methods=["GET"])
    
def projections():
    return jsonify({"status": "projections"}), 200

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

def graph():
    if request.method != "GET":
        return jsonify({"status":"error","message":"Method not allowed."}), 405

    try:
        try:
            userid = current_user.id
        except:
            return graph_error("Could not Retrieve User Data")
        transactions = Transactions.query.filter_by(userid=userid).all()
        financials = Financials.query.filter_by(userid=userid).first()

        if not transactions:
            return graph_error("No Transactions")
        else:
            category_totals = {}
            categories = []

            for transaction in transactions:
                category = transaction.category
                amount = transaction.amount if transaction.amount is not None else 0
                
                if category in category_totals:
                    category_totals[category] += amount
                else:
                    category_totals[category] = amount
                    categories.append(category)

            budget_amounts = []
            filtered_categories = []

            for category in categories:                
                budget = getattr(financials, category.lower(), None) 
                
                if budget is not None:
                    budget_amounts.append(budget)
                    filtered_categories.append(category)
                else:
                    budget_amounts.append(0)
                    filtered_categories.append(category)

            actual_amounts = [category_totals[category] for category in filtered_categories]

            if not filtered_categories:
                return graph_error("Budget not Completed")
            else:
                x = range(len(filtered_categories))

                fig, ax = plt.subplots()
                bars_actual = ax.bar(x, actual_amounts, label='Spent', color='green')
                for i in range(len(filtered_categories)):
                    if actual_amounts[i] > budget_amounts[i]:
                        ax.bar(x[i], actual_amounts[i] - budget_amounts[i], bottom=budget_amounts[i], color='red', label='Over Budget' if 'Over Budget' not in ax.get_legend_handles_labels()[1] else "")
                    else:
                        ax.bar(x[i], budget_amounts[i] - actual_amounts[i], bottom=actual_amounts[i], color='blue', label='Under Budget' if 'Under Budget' not in ax.get_legend_handles_labels()[1] else "")

                ax.set_ylabel('$')
                ax.set_title('Category Expenditure vs Budget')
                ax.set_xticks(x)
                ax.set_xticklabels(filtered_categories)                
                handles, labels = ax.get_legend_handles_labels()
                unique_labels = dict(zip(labels, handles))  
                ax.legend(unique_labels.values(), unique_labels.keys())
                plt.tight_layout()
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                plt.close()

    except Exception as e:
        return graph_error(f"Exception: {e}")
    return send_file(img, mimetype='image/png')

def habits():
    if request.method != "GET":
        return jsonify({"status":"error","message":"Method not allowed."}), 405
    try:
        userid = current_user.id
        transactions = Transactions.query.filter_by(userid=userid).all()
        financials = Financials.query.filter_by(userid=userid).first()
    except Exception:
        return jsonify({"status":"error","message":"Failed to Get User Data"}), 400
    
    if not transactions:
        return jsonify({"status": "error","message":"No Transactions"}), 400
    
    nothabits = {"rent", "goal1", "goal2", "goal3", "utilities"}
    purchases = set()
    habits = {}

    for transaction in transactions:
        item = (transaction.category, transaction.amount)
        
        if transaction.category.lower() in nothabits:
            continue 

        if item in purchases:
            if item in habits:
                habits[item] += 1
            else:
                habits[item] = 1
        else:
            purchases.add(item)

    if habits:
        total = 0
        message = []
        for (category, amount), count in habits.items():
            total += amount * count
            message.append(f"{category}: {amount} (x{count})\n")

        return jsonify({"status": "success", "message": f"Additional Cost: ${total}", "projections": message}), 200

    return jsonify({"status": "success", "message": "Additional Cost: $0", "projections":"No Habits Identified"}), 200