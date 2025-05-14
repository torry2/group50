from flask import jsonify, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import User, Financials, Transactions
import datetime

ENDPOINT = "share"

shares_storage = []

def share_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", "share-budget", share_budget_route, methods=["GET", "POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/list", "list-shares", list_shares_route, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/view/<int:share_id>", "view-shared-goal", view_shared_goal, methods=["GET"])
    
def share_budget_route():
    if request.method == "GET":
        goal_id = request.args.get('goal')
        return render_template("share.html", goal_id=goal_id)
    
    elif request.method == "POST":
        try:
            
            data = request.form
            username = data.get("username")
            message = data.get("message", "")

            # xss hotfix
            allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            cleanmessage = ''.join(char for char in message if char in allowlist)
            message = cleanmessage
            
            if not username:
                return jsonify({"status": "error", "message": "Username is required"}), 400
                
            user_to_share = User.query.filter_by(username=username).first()
            if not user_to_share:
                return jsonify({"status": "error", "message": f"User '{username}' not found"}), 404
                
            if user_to_share.id == current_user.id:
                return jsonify({"status": "error", "message": "Cannot share with yourself"}), 400
            
            new_share = {
                "id": len(shares_storage) + 1,
                "owner_id": current_user.id,
                "owner_username": current_user.username,
                "shared_with_id": user_to_share.id,
                "shared_with_username": user_to_share.username,
                "share_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "share_goals": True,
                "share_goal1": "share_goal1" in data,
                "share_goal2": "share_goal2" in data,
                "share_goal3": "share_goal3" in data,
                "message": message
            }
            
            shares_storage.append(new_share)
            
            return jsonify({
                "status": "success", 
                "message": f"Saving goals shared with {username} successfully!"
            }), 201
            
        except Exception as e:
            
            return jsonify({"status": "error", "message": str(e)}), 500

def list_shares_route():
    try:
        my_shares = [share for share in shares_storage if share["owner_id"] == current_user.id]
        shared_with_me = [share for share in shares_storage if share["shared_with_id"] == current_user.id]
        
        return jsonify({
            "status": "success",
            "my_shares": my_shares,
            "shared_with_me": shared_with_me
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def view_shared_goal(share_id):
    try:
        share = next((s for s in shares_storage if s["id"] == share_id), None)
        
        if not share:
            return jsonify({"status": "error", "message": "Share not found"}), 404
            
        if share["shared_with_id"] != current_user.id and share["owner_id"] != current_user.id:
            return jsonify({"status": "error", "message": "You don't have permission to view this share"}), 403
        
        goals_data = []
        owner_id = share["owner_id"]
        
        owner_financial = Financials.query.filter_by(userid=owner_id).first()
        
        if not owner_financial:
            return jsonify({"status": "error", "message": "Financial data not found"}), 404
        
        transactions = Transactions.query.filter_by(userid=owner_id).all()
    
        transaction_list = []
        for transaction in transactions:
            transaction_list.append({
                "id": transaction.id, 
                "name": transaction.name, 
                "category": transaction.category, 
                "amount": float(transaction.amount)
            })
        
        goal_totals = {
            "goal1": 0.0,
            "goal2": 0.0,
            "goal3": 0.0
        }
        
        for transaction in transaction_list:
            category = transaction["category"]
            amount = float(transaction["amount"])
            
            if category == "goal1" or category == "Goal 1":
                goal_totals["goal1"] += amount
            elif category == "goal2" or category == "Goal 2":
                goal_totals["goal2"] += amount
            elif category == "goal3" or category == "Goal 3":
                goal_totals["goal3"] += amount
        
        for i in range(1, 4):
            share_goal_attr = f"share_goal{i}"
            
            if share.get(share_goal_attr, False):
                goal_attr = f"goal{i}"
                
                target = float(getattr(owner_financial, goal_attr, 0) or 0.0)
                current_amount = goal_totals.get(goal_attr, 0.0)

                if target > 0:
                    progress = min(100, round((current_amount / target) * 100))
                else:
                    progress = 0

                goals_data.append({
                    "id": i,
                    "amount": current_amount,
                    "target": target,
                    "progress": progress,
                    "name": f"Goal {i}"
                })
        
        return jsonify({
            "status": "success",
            "share": share,
            "goals": goals_data
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500