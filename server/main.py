from fastapi.routing import APIRouter
from datetime import datetime, timedelta
from pydantic.dataclasses import dataclass
from dataclasses import field
from typing import Optional
from .smc_db import get_menu
from .models import FeedBack

router = APIRouter()

@dataclass
class FeedbackData:
    product_id: int
    feedback: str
    username: str

@dataclass
class DateRange:
    year: int = field(default_factory=lambda: datetime.now().year)
    month: int = field(default_factory=lambda: datetime.now().month)
    day: int = field(default_factory=lambda: datetime.now().day)

@router.get("/")
async def root():
    return {"message": "SMC cybercell api"}


@router.get("/menu/")
async def menu():
    menu_items = await get_menu()
    return {"menuItems": menu_items}


@router.post("/feedback/")
async def submit_feedback(data: FeedbackData) -> dict:
    await FeedBack.create(
            product_id=data.product_id,
            username=data.username,
            feedback=data.feedback)
    return {"success": "Feedback has been submitted"}


@router.get("/get-feedback/")
async def show_feedbacks(after: Optional[datetime] = None, before: Optional[datetime] = None):
    """
    date range if provided: ISO 8601
    """
    if after is None:
        after = datetime.now() + timedelta(days=-1)
    if before is None:
        before = datetime.now()
    return await (
            FeedBack
            .filter(datetime__gte=datetime(year=after.year,month=after.month,day=after.day))
            .filter(datetime__lte=datetime(year=before.year,month=before.month,day=before.day))
            )
