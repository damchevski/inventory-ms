from app import db


class ProductBuy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    image = db.Column(db.String)
    discountValid = db.Column(db.Date)
    discountPercentage = db.Column(db.Integer)


class ProductRent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String)
    image = db.Column(db.String)
    discountValid = db.Column(db.Date)
    discountPercentage = db.Column(db.Integer)


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class ReservedProductBuy(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    shopping_cart_id = db.Column(db.Integer, nullable=False)


class ReservedProductRent(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

