from flask import jsonify, request
from app.forms import *
from app import db
from app.models import Transactions, Financials
from flask_login import current_user

ENDPOINT = "data"

def data_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}/add-transaction", "add-transaction", add_transaction, methods=["POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/get-transactions", "get-transactions", get_transactions, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/delete-transaction/<int:transaction_id>", "delete-transaction", delete_transaction, methods=["DELETE"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/set-income-budget", "set-income-budget", set_inc_budget, methods=["POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/get-income-budget", "get-income-budget", get_inc_budget, methods=["GET"])
    
def add_transaction():
    if request.method != "POST":
        return jsonify({"status":"error","message":"Method not allowed."}), 405
    
    form = TransactionForm(request.form)
    if not form.validate_on_submit():
        return jsonify({"status":"error","errors": form.errors}), 400
    name = form.name.data
    category = form.category.data
    amount = form.amount.data

    if None in (name, category, amount):
        return jsonify({"status":"error","message":"Missing required fields."}), 400
    
    transaction = Transactions(userid=current_user.id, name=name, category=category, amount=amount)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"status": "success", "message": "Transaction added."}), 201

def get_transactions():
    if request.method != "GET":
        return jsonify({"status":"error","message":"Method not allowed."}), 405

    transaction_list = []
    transactions = Transactions.query.filter_by(userid=current_user.id).all()
    for transaction in transactions:
        transaction_list.append({"id": transaction.id, "name": transaction.name, "category": transaction.category, "amount": transaction.amount})

    return jsonify({"status": "success", "transactions": transaction_list}), 200

def delete_transaction(transaction_id):
    if request.method != "DELETE":
        return jsonify({"status":"error","message":"Method not allowed."}), 405

    transaction = Transactions.query.filter_by(id=transaction_id, userid=current_user.id).first()
    if not transaction:
        return jsonify({"status": "error", "message": "Transaction not found."}), 404
    
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"status": "success", "message": "Transaction deleted."}), 200

def set_inc_budget():
    if request.method != "POST":
        return jsonify({"status":"error","message":"Method not allowed."}), 405

    form = IncomeBudgetForm(request.form)
    if not form.validate_on_submit():
        return jsonify({"status":"error","errors": form.errors}), 400

    income = form.income.data
    food_budget = form.food_budget.data
    rent_budget = form.rent_budget.data
    utilities_budget = form.utilities_budget.data
    shopping_budget = form.shopping_budget.data
    entertainment_budget = form.entertainment_budget.data
    other_budget = form.other_budget.data
    goal1_budget = form.goal1_budget.data
    goal2_budget = form.goal2_budget.data
    goal3_budget = form.goal3_budget.data

    if None in (income, food_budget, rent_budget, utilities_budget, shopping_budget, entertainment_budget, other_budget, goal1_budget, goal2_budget, goal3_budget):
        return jsonify({"status":"error","message":"Missing required fields."}), 400

    inc_budget = Financials.query.filter_by(userid=current_user.id).first()
    if not inc_budget:
        inc_budget = Financials(userid=current_user.id, income=income, currency="AUD", food=food_budget, rent=rent_budget, utilities=utilities_budget, shopping=shopping_budget, entertainment=entertainment_budget, other=other_budget, goal1=goal1_budget, goal2=goal2_budget, goal3=goal3_budget)
        db.session.add(inc_budget)
        db.session.commit()
        return jsonify({"status": "success", "message": "Income and budgets set."}), 200
    else:
        inc_budget.income = income
        inc_budget.currency = "AUD"
        inc_budget.food = food_budget
        inc_budget.rent = rent_budget
        inc_budget.utilities = utilities_budget
        inc_budget.shopping = shopping_budget
        inc_budget.entertainment = entertainment_budget
        inc_budget.other = other_budget
        inc_budget.goal1 = goal1_budget
        inc_budget.goal2 = goal2_budget
        inc_budget.goal3 = goal3_budget
        db.session.commit()
        return jsonify({"status": "success", "message": "Income and budgets updated."}), 200
    
def get_inc_budget():
    if request.method != "GET":
        return jsonify({"status":"error","message":"Method not allowed."}), 405
    
    inc_budget = Financials.query.filter_by(userid=current_user.id).first()
    if not inc_budget:
        default = {
            "income": 0,
            "currency": "AUD",
            "food": 0,
            "rent": 0,
            "utilities": 0,
            "shopping": 0,
            "entertainment": 0,
            "other": 0,
            "goal1": 0,
            "goal2": 0,
            "goal3": 0
        }
        return jsonify({"status": "success", "income_budget": default}), 200
    
    inc_budget_data = {
        "income": float(inc_budget.income),
        "currency": inc_budget.currency,
        "food": float(inc_budget.food),
        "rent": float(inc_budget.rent),
        "utilities": float(inc_budget.utilities),
        "shopping": float(inc_budget.shopping),
        "entertainment": float(inc_budget.entertainment),
        "other": float(inc_budget.other),
        "goal1": float(inc_budget.goal1),
        "goal2": float(inc_budget.goal2),
        "goal3": float(inc_budget.goal3)
    }
    return jsonify({"status": "success", "income_budget": inc_budget_data}), 200