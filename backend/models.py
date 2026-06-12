from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from backend.database import Base

class WatchStatus(enum.Enum):
    in_stock    = "in_stock"
    reserved    = "reserved"
    sold        = "sold"
    consignment = "consignment"


class WatchCondition(enum.Enum):
    new = "new"
    like_new = "like_new"
    very_good = "very_good"
    good = "good"
    fair = "fair"


class Watch(Base):
    __tablename__ = "watches"
    id             = Column(Integer, primary_key=True)
    model          = Column(String, nullable=False)   # e.g. Rolex Daytona
    reference      = Column(String)                   # e.g. 116500LN
    serial         = Column(String)
    purchase_price = Column(Float)
    target_price   = Column(Float)
    currency       = Column(String, default="EUR")
    location       = Column(String)                   # who has it
    status         = Column(Enum(WatchStatus), default=WatchStatus.in_stock)
    purchased_by   = Column(String)                   # which partner
    purchased_from = Column(String)                   # source/dealer
    notes          = Column(String)
    created_at     = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at     = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    photos         = relationship("Photo", back_populates="watch")
    condition = Column(Enum(WatchCondition), default=WatchCondition.very_good)


class Photo(Base):
    __tablename__ = "photos"
    id         = Column(Integer, primary_key=True)
    watch_id   = Column(Integer, ForeignKey("watches.id"))
    file_path  = Column(String)
    photo_type = Column(String, default="watch")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    watch      = relationship("Watch", back_populates="photos")

class Sale(Base):
    __tablename__ = "sales"
    id           = Column(Integer, primary_key=True)
    watch_id     = Column(Integer, ForeignKey("watches.id"))
    sale_price   = Column(Float)
    sold_by      = Column(String)
    sold_at      = Column(DateTime, default=lambda: datetime.now(timezone.utc))