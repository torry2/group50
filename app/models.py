from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

# List of valid categories, this field is not normalised as therefore not consistent across tables, - use this list to check validity!
CATEGORIES = ["food", "rent", "utilities", "shopping", "entertainment", "other", "goal1", "goal2", "goal3"]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<Transactions {self.id} – {self.userid})>"

class Financials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    income = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(200), nullable=False)

    # budget (categories: see note at top of file)
    food = db.Column(db.Numeric(10, 2))
    rent = db.Column(db.Numeric(10, 2))
    utilities = db.Column(db.Numeric(10, 2))
    shopping = db.Column(db.Numeric(10, 2))
    entertainment = db.Column(db.Numeric(10, 2))
    other = db.Column(db.Numeric(10, 2))
    goal1 = db.Column(db.Numeric(10, 2))
    goal2 = db.Column(db.Numeric(10, 2))
    goal3 = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f"<Financials {self.id} – {self.userid})>"