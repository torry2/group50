from datetime import datetime, timezone
from typing import Optional
import uuid
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = (
        sa.CheckConstraint("amount >= 0", name="ck_transaction_amount_nonnegative"),
    )

    id = db.Column(
        sa.dialects.postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True
    )
    user_id = db.Column(
        sa.dialects.postgresql.UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    amount = db.Column(
        sa.Numeric(10, 2),
        nullable=False
    )
    currency = db.Column(
        sa.String(3),
        nullable=False,
        server_default=sa.text("'AUD'")
    )
    description = db.Column(
        sa.Text,
        nullable=True
    )
    status = db.Column(
        sa.Enum("pending", "completed", "failed", name="transaction_status"),
        nullable=False,
        server_default=sa.text("'pending'")
    )
    transaction_date = db.Column(
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now()
    )
    created_at = db.Column(
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now()
    )

    def __repr__(self):
        return f"<Transaction {self.id} – {self.amount} {self.currency} ({self.status})>"

