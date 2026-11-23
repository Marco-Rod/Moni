import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, IdMixin, TimestampMixin

MONEY = Numeric(14, 2)


def _enum(e: type[enum.Enum]) -> Enum:
    return Enum(e, native_enum=False, length=20, values_callable=lambda x: [m.value for m in x])


class FlowKind(enum.StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class Nature(enum.StrEnum):
    FIXED = "fixed"
    VARIABLE = "variable"
    EXTRA = "extra"


class CreditorType(enum.StrEnum):
    BANK = "bank"
    FINANCIAL = "financial"
    PERSON = "person"
    OTHER = "other"


class DebtStatus(enum.StrEnum):
    ACTIVE = "active"
    PAID = "paid"


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    currency: Mapped[str] = mapped_column(String(3), default="MXN")


class Category(Base, IdMixin, TimestampMixin):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "name", "kind"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(80))
    kind: Mapped[FlowKind] = mapped_column(_enum(FlowKind))


class RecurringObligation(Base, IdMixin, TimestampMixin):
    """Pagos mensuales: luz, agua, internet, renta, suscripciones."""

    __tablename__ = "recurring_obligations"
    __table_args__ = (CheckConstraint("due_day BETWEEN 1 AND 31", name="due_day_range"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String(120))
    estimated_amount: Mapped[Decimal] = mapped_column(MONEY)
    currency: Mapped[str] = mapped_column(String(3), default="MXN")
    due_day: Mapped[int]
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Transaction(Base, IdMixin, TimestampMixin):
    __tablename__ = "transactions"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("categories.id"))
    obligation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("recurring_obligations.id")
    )
    kind: Mapped[FlowKind] = mapped_column(_enum(FlowKind))
    nature: Mapped[Nature] = mapped_column(_enum(Nature), default=Nature.VARIABLE)
    amount: Mapped[Decimal] = mapped_column(MONEY)
    currency: Mapped[str] = mapped_column(String(3), default="MXN")
    occurred_on: Mapped[date] = mapped_column(Date, index=True)
    description: Mapped[str | None] = mapped_column(Text)


class Debt(Base, IdMixin, TimestampMixin):
    __tablename__ = "debts"
    __table_args__ = (
        CheckConstraint("current_balance >= 0", name="balance_non_negative"),
        CheckConstraint("original_amount > 0", name="original_positive"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    creditor: Mapped[str] = mapped_column(String(120))
    creditor_type: Mapped[CreditorType] = mapped_column(_enum(CreditorType))
    original_amount: Mapped[Decimal] = mapped_column(MONEY)
    current_balance: Mapped[Decimal] = mapped_column(MONEY)
    currency: Mapped[str] = mapped_column(String(3), default="MXN")
    annual_rate_pct: Mapped[Decimal | None] = mapped_column(Numeric(7, 4))
    minimum_payment: Mapped[Decimal | None] = mapped_column(MONEY)
    due_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[DebtStatus] = mapped_column(_enum(DebtStatus), default=DebtStatus.ACTIVE)
    notes: Mapped[str | None] = mapped_column(Text)


class DebtPayment(Base, IdMixin, TimestampMixin):
    __tablename__ = "debt_payments"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    debt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("debts.id"), index=True
    )
    amount: Mapped[Decimal] = mapped_column(MONEY)
    paid_on: Mapped[date] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)


class Budget(Base, IdMixin, TimestampMixin):
    """Límite mensual por categoría. `month` = primer día del mes."""

    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "month"),
        CheckConstraint("limit_amount >= 0", name="limit_non_negative"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"))
    month: Mapped[date] = mapped_column(Date)
    limit_amount: Mapped[Decimal] = mapped_column(MONEY)
