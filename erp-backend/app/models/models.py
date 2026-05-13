import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict,Any
from sqlalchemy import Column, JSON, Numeric
from sqlmodel import Field, Relationship, SQLModel


class EUserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEACTIVE = "ACTIVE"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: Optional[str] = Field(default=None, unique=True, max_length=255)
    email: Optional[str] = Field(default=None, unique=True, max_length=255)
    phone: Optional[str] = Field(default=None, unique=True, max_length=255)
    password: str = Field(max_length=1000)
    status: EUserStatus = Field(default=EUserStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user_roles: List["UserRole"] = Relationship(back_populates="user")
    sessions: List["Session"] = Relationship(back_populates="user")


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", unique=True)
    role_id: str = Field(foreign_key="roles.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    role: "Role" = Relationship(back_populates="user_roles")
    user: "User" = Relationship(back_populates="user_roles")


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user_roles: List["UserRole"] = Relationship(back_populates="role")


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    userId: Optional[str] = Field(default=None, foreign_key="users.id")
    source: Optional[str] = None
    rawText: str = Field()
    parsed: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="sessions")
    items: List["Item"] = Relationship(back_populates="session")
    sale: Optional["Sale"] = Relationship(back_populates="session")


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sessionId: str = Field(foreign_key="sessions.id")
    name: str = Field()
    normalizedName: Optional[str] = None
    qty: int = Field(default=1)
    unitPrice: Decimal = Field(default=Decimal("0"))
    subtotal: Decimal = Field(default=Decimal("0"))
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    session: "Session" = Relationship(back_populates="items")


class Sale(SQLModel, table=True):
    __tablename__ = "sales"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sessionId: str = Field(foreign_key="sessions.id", unique=True)
    totalAmount: Decimal = Field(default=Decimal("0"))
    profit: Decimal = Field(default=Decimal("0"))
    profitMargin: Optional[Decimal] = Field(default=None)
    currency: str = Field(default="idr")
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    session: "Session" = Relationship(back_populates="sale")


class EProductUnit(str, Enum):
    PCS = "pcs"
    KG = "kg"
    LITER = "liter"
    METER = "meter"
    BOX = "box"
    PACK = "pack"


class ETransactionType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTMENT = "adjustment"
    RETURN_IN = "return_in"
    RETURN_OUT = "return_out"


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(unique=True, max_length=255)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    products: List["Product"] = Relationship(back_populates="category")


class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    stock_ins: List["StockIn"] = Relationship(back_populates="supplier")


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    stock_outs: List["StockOut"] = Relationship(back_populates="customer")


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sku: Optional[str] = Field(default=None, unique=True, max_length=50)
    name: str = Field(max_length=255)
    description: Optional[str] = None
    category_id: Optional[str] = Field(default=None, foreign_key="categories.id")
    unit: EProductUnit = Field(default=EProductUnit.PCS)
    cost_price: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    selling_price: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    min_stock: int = Field(default=0)
    image_url: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    category: Optional["Category"] = Relationship(back_populates="products")
    stock_in_items: List["StockInItem"] = Relationship(back_populates="product")
    stock_out_items: List["StockOutItem"] = Relationship(back_populates="product")
    stock_transactions: List["StockTransaction"] = Relationship(back_populates="product")


class StockIn(SQLModel, table=True):
    __tablename__ = "stock_ins"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_number: Optional[str] = Field(default=None, unique=True, max_length=50)
    supplier_id: str = Field(foreign_key="suppliers.id")
    total_amount: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    supplier: "Supplier" = Relationship(back_populates="stock_ins")
    items: List["StockInItem"] = Relationship(back_populates="stock_in")


class StockInItem(SQLModel, table=True):
    __tablename__ = "stock_in_items"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    stock_in_id: str = Field(foreign_key="stock_ins.id")
    product_id: str = Field(foreign_key="products.id")
    qty: int = Field(default=0)
    unit_price: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    subtotal: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    stock_in: "StockIn" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="stock_in_items")


class StockOut(SQLModel, table=True):
    __tablename__ = "stock_outs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_number: Optional[str] = Field(default=None, unique=True, max_length=50)
    customer_id: Optional[str] = Field(default=None, foreign_key="customers.id")
    total_amount: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    profit: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Optional["Customer"] = Relationship(back_populates="stock_outs")
    items: List["StockOutItem"] = Relationship(back_populates="stock_out")


class StockOutItem(SQLModel, table=True):
    __tablename__ = "stock_out_items"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    stock_out_id: str = Field(foreign_key="stock_outs.id")
    product_id: str = Field(foreign_key="products.id")
    qty: int = Field(default=0)
    unit_price: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    subtotal: Decimal = Field(default=Decimal("0"), sa_column=Column(Numeric(12, 2)))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    stock_out: "StockOut" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="stock_out_items")


class StockTransaction(SQLModel, table=True):
    __tablename__ = "stock_transactions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    product_id: str = Field(foreign_key="products.id")
    transaction_type: ETransactionType
    reference_id: Optional[str] = None
    qty_change: int
    qty_before: int
    qty_after: int
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    product: "Product" = Relationship(back_populates="stock_transactions")