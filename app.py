import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime


# endpoints
def create_product_buy(product_buy_body):
    product = db.session.query(ProductBuy).filter_by(name=product_buy_body['name']).first()

    if product:
        return {'error': '{} already exist'.format(id)}, 409

    product = ProductBuy(name=product_buy_body['name'], price=product_buy_body['price'],
                         description=product_buy_body['description'], image=product_buy_body['image'],
                         category=product_buy_body['category'], brand=product_buy_body['brand'],
                         quantity=product_buy_body['quantity'])

    db.session.add(product)
    db.session.commit()

    return {'id': product.id, 'name': product.name}


def create_product_rent(product_rent_body):
    product = ProductRent(name=product_rent_body['name'], price=product_rent_body['price'],
                          description=product_rent_body['description'], image=product_rent_body['image'],
                          category=product_rent_body['category'], brand=product_rent_body['brand'],
                          quantity=product_rent_body['available'])

    db.session.add(product)
    db.session.commit()

    return product


def edit_product_buy(id, product_buy_body):
    product = db.session.query(ProductBuy).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    product.name = product_buy_body['name']
    product.price = product_buy_body['price']
    product.description = product_buy_body['description']
    product.image = product_buy_body['image']
    product.category = product_buy_body['category']
    product.brand = product_buy_body['brand']
    product.quantity = product_buy_body['quantity']

    db.session.commit()

    return product


def edit_product_rent(id, product_rent_body):
    product = db.session.query(ProductRent).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    product.name = product_rent_body['name']
    product.price = product_rent_body['price']
    product.description = product_rent_body['description']
    product.image = product_rent_body['image']
    product.category = product_rent_body['category']
    product.brand = product_rent_body['brand']
    product.available = product_rent_body['available']

    db.session.commit()

    return product


def delete_product_buy(id):
    product = db.session.query(ProductBuy).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    db.session.delete(product)

    return product


def delete_product_rent(id):
    product = db.session.query(ProductRent).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    db.session.delete(product)

    return product


def set_product_buy_discount(id, discount_percentage, valid_until):
    product = db.session.query(ProductBuy).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    product.discountValid = valid_until
    product.discountPercentage = discount_percentage

    db.session.commit()

    return product


def set_product_rent_discount(id, discount_percentage, valid_until):
    product = db.session.query(ProductRent).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    product.discountValid = valid_until
    product.discountPercentage = discount_percentage

    db.session.commit()

    return product


def get_product_buy(id):
    product = db.session.query(ProductBuy).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    return product


def get_product_rent(id):
    product = db.session.query(ProductRent).filter_by(id=id).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    return product


def get_all_products_buy(id):
    products = db.Session.query(ProductBuy).all()
    return products


def get_all_products_rent(id):
    products = db.Session.query(ProductRent).all()
    return products


# Do tuka ----------------------------------------------------------------------

def search_product_buy(search_param):
    product = db.session.query(ProductBuy).filter_by(name=search_param).first()

    if not product:
        return {'error': '{} not found'.format(search_param)}, 404

    return {'id': product.id, 'name': product.name}


def search_product_rent(search_param):
    product = db.session.query(ProductRent).filter_by(name=search_param).first()

    if not product:
        return {'error': '{} not found'.format(id)}, 404

    return {'id': product.id, 'name': product.name}


def buy_coupon(id):
    coupon = db.Session.query(Coupon).filter_by(id=id).first()

    if not coupon:
        return {'error': '{ not found'.format(id)}, 404

    coupon.quantity = coupon.quantity - 1

    db.session.commit()

    return {'id': coupon.id}


def reserve_product_buy(reserve_product_buy_body):
    product = db.session.query(ProductBuy).filter_by(id=reserve_product_buy_body['product_id']).first()

    if not product:
        return {'error': '{} not found'.format(reserve_product_buy_body['product_id'])}, 404

    if product.quantity - reserve_product_buy_body['quantity'] < 0:
        return {'error': '{} > 0 quantity'.format(reserve_product_buy_body['product_id'])}, 500

    product.quantity = product.quantity - reserve_product_buy_body['quantity']
    reserved_product = ReservedProductBuy(product_id=reserve_product_buy_body['product_id'],
                                          quantity=reserve_product_buy_body['quantity'],
                                          shopping_cart_id=reserve_product_buy_body['shopping_cart_id'])

    db.session.add(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'shopping_cart_id': reserved_product.shopping_cart_id}


def reserve_product_rent(reserve_product_rent_body):
    product = db.session.query(ProductRent).filter_by(id=reserve_product_rent_body['product_id']).first()

    if not product:
        return {'error': '{} not found'.format(reserve_product_rent_body['product_id'])}, 404

    if not product.available:
        return {'error': '{} not available'.format(reserve_product_rent_body['product_id'])}, 500

    product.available = False
    reserved_product = ReservedProductBuy(product_id=reserve_product_rent_body['product_id'],
                                          user_id=reserve_product_rent_body['user_id'])

    db.session.add(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'user_id': reserved_product.user_id}


def buy_product(shopping_cart_id):
    reserved_product = db.session.query(ReservedProductBuy).filter_by(shopping_cart_id=shopping_cart_id).first()

    db.session.delete(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'shopping_cart_id': reserved_product.shopping_cart_id}


def rent_product(product_id, user_id):
    reserved_product = db.session.query(ReservedProductRent).filter_by(user_id=user_id).filter_by(
        product_id=product_id).first()

    db.delete(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'user_id': reserved_product.user_id}


def get_price_for_product_buy(product_id):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    if product.discountValid:
        if product.discountValid > datetime.datetime.now():
            return product.price - (product.price / 100 * product.discountPercentage)

    return product.price


def get_price_for_product_rent(product_id):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    if product.discountValid:
        if product.discountValid > datetime.datetime.now():
            return product.price - (product.price / 100 * product.discountPercentage)

    return product.price


# configuration
connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

# dummy reference for migrations on ly
from models.models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
