from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested
from models.models import *


class CouponSchema(SQLAlchemySchema):
    class Meta:
        model = Coupon
        include_relationships = True
        load_instance = True  # Optional: deserialize to model instances


