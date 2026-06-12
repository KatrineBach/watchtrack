from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from backend.models import WatchStatus, WatchCondition

class WatchCreate(BaseModel):
    """What you need to provide to create a watch. All optional except model."""
    model: str
    reference: Optional[str] = None
    serial: Optional[str] = None
    purchase_price: Optional[float] = None
    target_price: Optional[float] = None
    currency: str = "EUR"
    location: Optional[str] = None
    status: WatchStatus = WatchStatus.in_stock
    purchase_by: Optional[str] = None
    purchase_from: Optional[str] = None
    notes: Optional[str] = None
    condition: WatchCondition = WatchCondition.very_good

class WatchRead(WatchCreate):
    """What you get back when reading a watch — adds the DB-generated fields."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # lets Pydantic read SQLAlchemy objects

