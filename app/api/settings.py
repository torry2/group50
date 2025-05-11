from flask import jsonify, request, redirect, url_for
from app.forms import *
from app import db
from app.models import *
from flask_login import current_user, logout_user

ENDPOINT = "settings"

def settings_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", f"{prefix}/{ENDPOINT}", settings, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/delete", f"{prefix}/{ENDPOINT}/delete", delete_account, methods=["POST"])

def settings():
    return jsonify({"status": "settings"}), 200

def delete_account():
    sf = deleteForm()
    if not sf.validate_on_submit():
        return jsonify({"status":"error","errors": sf.errors}), 400
    try:
        userid = current_user.id
        Financials.query.filter_by(userid=userid).delete()
        Transactions.query.filter_by(userid=userid).delete()
        db.session.delete(current_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "success", "message":"Account Failed to Delete"}), 200
    return jsonify({"status": "success", "message":"Account Deleted"}), 200