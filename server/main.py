from fastapi.routing import APIRouter
from datetime import datetime, timedelta
from pydantic.dataclasses import dataclass
from typing import Optional
import asyncio
from .smc_db import get_menu, get_pname
from .models import FeedBack

router = APIRouter()

@dataclass
class FeedbackData:
    product_id: int
    product_name: str
    stars: int
    feedback: str
    username: str

@dataclass
class MenuItem:
    product_id: int
    name: str
    meal: int
    special: bool


@router.get("/")
async def root():
    return {"message": "SMC cybercell api"}


@router.get("/menu/", response_model=list[MenuItem])
async def menu():
    menu_items = await get_menu()
    return menu_items


@router.post("/feedback/")
async def submit_feedback(data: FeedbackData) -> dict:
    await FeedBack.create(
            product_id=data.product_id,
            product_name=data.product_name,
            stars=data.stars,
            username=data.username,
            feedback=data.feedback)
    return {"success": "Feedback has been submitted"}


@router.get("/get-feedback/")
async def show_feedbacks(after: Optional[datetime] = None, before: Optional[datetime] = None):
    """
    date range if provided: ISO 8601
    """
    if after is None:
        after = datetime.now() - timedelta(days=1)
    if before is None:
        before = datetime.now() + timedelta(days=1)

    feedback_list = await (
            FeedBack
            .filter(datetime__gte=datetime(year=after.year,month=after.month,day=after.day))
            .filter(datetime__lte=datetime(year=before.year,month=before.month,day=before.day))
            )
    return [i.feedback_json() for i in feedback_list]
