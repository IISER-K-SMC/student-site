
from tortoise import Tortoise, run_async, fields

from tortoise.models import Model

class FeedBack(Model):
    id = fields.IntField(pk=True)
    product_id = fields.IntField()
    username = fields.TextField()
    feedback = fields.TextField()
    datetime = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "feedback"

    def __str__(self):
        return f"{self.username}<{self.product_id}> {self.feedback}"
