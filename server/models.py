from tortoise import fields
from tortoise.models import Model

class FeedBack(Model):
    id = fields.IntField(pk=True)
    product_id = fields.IntField(index=True)
    product_name  = fields.TextField()
    stars = fields.IntField()
    uid = fields.CharField(max_length=50)
    feedback = fields.TextField()
    datetime = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "feedback"

    def __str__(self):
        return f"{self.uid}<{self.product_id}> {self.feedback}"

    def feedback_json(self):
        return {
            "datetime": self.datetime,
            "uid": self.uid,
            "stars": self.stars,
            "productName": self.product_name,
            "feedback": self.feedback,
        }

class Security(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=20, index=True, unique=True)
    uid = fields.CharField(max_length=50)
    login_datetime = fields.DatetimeField(auto_now=True)
