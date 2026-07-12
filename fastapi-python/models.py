from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class DateRange(BaseModel):
    from_: Optional[str] = Field(default=None, alias="from")
    to: Optional[str] = None

    class Config:
        populate_by_name = True


class AmountRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None


class TransactionSearchRequest(BaseModel):
    dateRange: Optional[DateRange] = None
    amountRange: Optional[AmountRange] = None
    status: Optional[List[str]] = None
    paymentMethod: Optional[List[str]] = None
    customerEmail: Optional[EmailStr] = None
    cardLast4: Optional[str] = None
    merchantId: Optional[str] = None
    currency: Optional[str] = None
    page: int = 1
    pageSize: int = 20
