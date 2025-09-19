from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Category(str, Enum):
    VORSPEISEN = "Vorspeisen"
    HAUPTGERICHTE = "Hauptgerichte"
    DESSERTS = "Desserts"


# MenuItem Models
class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: Category
    name: str
    description: str
    price: float = Field(..., ge=0)
    image: str
    available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('price')
    def validate_price(cls, v):
        return round(v, 2)


class MenuItemCreate(BaseModel):
    category: Category
    name: str
    description: str
    price: float = Field(..., ge=0)
    image: str
    available: bool = True

    @validator('price')
    def validate_price(cls, v):
        return round(v, 2)


# Order Models
class OrderItem(BaseModel):
    menu_item_id: str
    name: str
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=1)

    @validator('price')
    def validate_price(cls, v):
        return round(v, 2)


class Customer(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)

    @validator('phone')
    def validate_phone(cls, v):
        # Remove all non-digit characters
        phone_digits = ''.join(filter(str.isdigit, v))
        
        # Swiss phone number validation (basic)
        if len(phone_digits) < 10:
            raise ValueError('Phone number too short')
        
        return v.strip()

    @validator('name')
    def validate_name(cls, v):
        return v.strip()


class OrderCreate(BaseModel):
    items: List[OrderItem]
    customer: Customer
    pickup_time: datetime
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Order must contain at least one item')
        return v

    @validator('pickup_time')
    def validate_pickup_time(cls, v):
        if v <= datetime.utcnow():
            raise ValueError('Pickup time must be in the future')
        return v


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    items: List[OrderItem]
    customer: Customer
    pickup_time: datetime
    total: float = Field(..., ge=0)
    status: OrderStatus = OrderStatus.PENDING
    order_number: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('total')
    def validate_total(cls, v):
        return round(v, 2)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


# Newsletter Models
class NewsletterSubscription(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    is_active: bool = True
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    unsubscribed_at: Optional[datetime] = None


class NewsletterSubscribe(BaseModel):
    email: EmailStr


class NewsletterResponse(BaseModel):
    message: str
    subscription: Optional[dict] = None


# Response Models
class ErrorResponse(BaseModel):
    error: dict


class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None