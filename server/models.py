from tortoise import fields
from tortoise.models import Model

class FeedBack(Model):
    id = fields.IntField(pk=True)
    product_id = fields.IntField(index=True)
    product_name  = fields.TextField()
    stars = fields.IntField()
    username = fields.TextField()
    feedback = fields.TextField()
    datetime = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "feedback"

    def __str__(self):
        return f"{self.username}<{self.product_id}> {self.feedback}"

    def feedback_json(self):
        return {
            "datetime": self.datetime,
            "username": self.username,
            "stars": self.stars,
            "productName": self.product_name,
            "feedback": self.feedback,
        }
