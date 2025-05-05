from flask import jsonify, request
from app.forms import *
from app import db
from app.models import Transactions
from flask_login import current_user

ENDPOINT = "data"

def data_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}/add", "add", add_transaction, methods=["POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/get", "get", get_transactions, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/delete/<int:transaction_id>", "delete", delete_transaction, methods=["DELETE"])
    
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