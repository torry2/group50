import uuid
from sqlalchemy import (
    Column, String, Text, Date, ForeignKey, 
    CheckConstraint, Enum, Numeric, func, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    date_of_birth = Column(Date)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    # one-to-many: a user can have many transactions
    transactions = relationship("Transaction", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_transaction_amount_nonnegative"),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(
        String(3),
        nullable=False,
        server_default=text("'AUD'")
    )
    description = Column(Text)
    status = Column(
        Enum("pending", "completed", "failed", name="transaction_status"),
        nullable=False,
        server_default=text("'pending'")
    )
    transaction_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    
    )

    # relationship back to User
    user = relationship("User", back_populates="transactions")
