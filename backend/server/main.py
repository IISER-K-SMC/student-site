from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from .security import get_current_user
from pydantic.dataclasses import dataclass

from .models import FeedBack
from . import smc_db_aio


router = APIRouter()

@dataclass
class FeedbackData:
    product_id: int
    product_name: str
    stars: int
    feedback: str

@dataclass
class MenuItem:
    product_id: int
    name: str
    meal: int
    special: bool


@router.get("/")
async def root():
    return {"message": "SMC cybercell api"}


@router.get("/menu", response_model=list[MenuItem])
async def menu():
    menu_items = await smc_db_aio.get_menu()
    return menu_items


@router.post("/feedback")
async def submit_feedback(
        data: FeedbackData,
        uid = Depends(get_current_user)) -> dict:
    await FeedBack.create(
            product_id=data.product_id,
            product_name=data.product_name,
            stars=data.stars,
            uid=uid,
            feedback=data.feedback)
    return {"success": "Feedback has been submitted"}

@router.get("/orders")
async def orders(uid = Depends(get_current_user)):
    return await smc_db_aio.get_past_orders(uid)


@router.get("/get-feedback")
async def show_feedbacks(after: Optional[datetime] = None,
                        before: Optional[datetime] = None,
                        ):
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
