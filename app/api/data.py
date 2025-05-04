from flask import jsonify, request
from app.forms import *
from app import db
from app.models import Transactions
from flask_login import current_user

ENDPOINT = "data"

def data_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}/add", "add", add_transaction, methods=["POST"])
    
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