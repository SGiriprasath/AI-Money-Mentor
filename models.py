"""Database models and persistence layer for AI-Money-Mentor.

Replaces the previous module-level in-memory lists (expense_data,
assets_data, liabilities_data) with SQLite-backed storage via
Flask-SQLAlchemy, so data survives server restarts.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(40), nullable=False)
    
    # New AI fields
    ai_confidence = db.Column(db.Float, default=0.0)  # AI confidence score
    user_corrected = db.Column(db.Boolean, default=False)  # Was this corrected by user?
    original_ai_category = db.Column(db.String(120), nullable=True)  # What AI originally said
    is_subscription = db.Column(db.Boolean, default=False)
    is_recurring = db.Column(db.Boolean, default=False)
    is_anomaly = db.Column(db.Boolean, default=False)
    merchant_name = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
            "ai_confidence": self.ai_confidence,
            "user_corrected": self.user_corrected,
            "is_subscription": self.is_subscription,
            "is_recurring": self.is_recurring,
            "is_anomaly": self.is_anomaly
        }


class Asset(db.Model):
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self, index):
        # Original shape: {"id", "name", "amount"} where id was the list index.
        # Frontend deletes by list position, so we expose the positional index as id.
        return {"id": index, "name": self.name, "amount": self.amount}


class Liability(db.Model):
    __tablename__ = "liabilities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self, index):
        return {"id": index, "name": self.name, "amount": self.amount}