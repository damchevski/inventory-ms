import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# endpoints
def create_coupon(coupon_body):
    coupon = Coupon(type=coupon_body['type'], quantity=coupon_body['quantity'])

    db.session.add(coupon)
    db.session.commit()

    return {'coupon_id': coupon.id, 'type': coupon.type, 'quantity': coupon.quantity}


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

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'quantity': product.quantity}


def create_product_rent(product_rent_body):
    product = db.session.query(ProductRent).filter_by(name=product_rent_body['name']).first()

    if product:
        return {'error': '{} already exist'.format(id)}, 409

    product = ProductRent(name=product_rent_body['name'], price=product_rent_body['price'],
                          description=product_rent_body['description'], image=product_rent_body['image'],
                          category=product_rent_body['category'], brand=product_rent_body['brand'],
                          available=product_rent_body['available'])

    db.session.add(product)
    db.session.commit()

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'available': product.available}


def edit_product_buy(product_id, product_buy_body):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    product.name = product_buy_body['name']
    product.price = product_buy_body['price']
    product.description = product_buy_body['description']
    product.image = product_buy_body['image']
    product.category = product_buy_body['category']
    product.brand = product_buy_body['brand']
    product.quantity = product_buy_body['quantity']

    db.session.commit()

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'quantity': product.quantity}


def edit_product_rent(product_id, product_rent_body):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    product.name = product_rent_body['name']
    product.price = product_rent_body['price']
    product.description = product_rent_body['description']
    product.image = product_rent_body['image']
    product.category = product_rent_body['category']
    product.brand = product_rent_body['brand']
    product.available = product_rent_body['available']

    db.session.commit()

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'available': product.available}


def delete_product_buy(product_id):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    db.session.delete(product)
    db.session.commit()

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'quantity': product.quantity}


def delete_product_rent(product_id):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    db.session.delete(product)
    db.session.commit()

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'available': product.available}


def set_product_buy_discount(product_id, discount_percentage, valid_until):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    product.discountValid = datetime.strptime(valid_until, "%d-%m-%Y").date()
    product.discountPercentage = discount_percentage

    db.session.commit()

    return {'id': product.id, 'name': product.name,
            'discount_percentage': product.discountPercentage,
            'discount_valid_until': product.discountValid}


def set_product_rent_discount(product_id, discount_percentage, valid_until):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    product.discountValid = datetime.strptime(valid_until, "%d-%m-%Y").date()
    product.discountPercentage = discount_percentage

    db.session.commit()

    return {'id': product.id, 'name': product.name,
            'discount_percentage': product.discountPercentage,
            'discount_valid_until': product.discountValid}


def get_product_buy(product_id):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'quantity': product.quantity}


def get_product_rent(product_id):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'available': product.available}


def get_all_products_buy():
    products = db.session.query(ProductBuy).all()
    itemsList = []

    for product in products:
        itemsList.append({'id': product.id,
                          'name': product.name,
                          'price': product.price,
                          'description': product.description,
                          'image': product.image,
                          'category': product.category,
                          'brand': product.brand,
                          'quantity': product.quantity})

    return itemsList


def get_all_products_rent():
    products = db.session.query(ProductRent).all()
    itemsList = []

    for product in products:
        itemsList.append({'id': product.id,
                          'name': product.name,
                          'price': product.price,
                          'description': product.description,
                          'image': product.image,
                          'category': product.category,
                          'brand': product.brand,
                          'available': product.available})

    return itemsList


def search_product_buy(search_param):
    product = db.session.query(ProductBuy).filter_by(name=search_param).first()

    if not product:
        return {'error': '{} not found'.format(search_param)}, 404

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'quantity': product.quantity}


def search_product_rent(search_param):
    product = db.session.query(ProductRent).filter_by(name=search_param).first()

    if not product:
        return {'error': '{} not found'.format(search_param)}, 404

    return {'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'brand': product.brand,
            'available': product.available}


def buy_coupon(coupon_id):
    coupon = db.session.query(Coupon).filter_by(id=coupon_id).first()

    if not coupon:
        return {'error': '{ not found'.format(coupon_id)}, 404

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
    reserved_product = ReservedProductRent(product_id=reserve_product_rent_body['product_id'],
                                           user_id=reserve_product_rent_body['user_id'])

    db.session.add(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'user_id': reserved_product.user_id}


def buy_product(shopping_cart_id):
    reserved_products = db.session.query(ReservedProductBuy).filter_by(shopping_cart_id=shopping_cart_id).all()

    items = []
    for reserved_product in reserved_products:
        db.session.delete(reserved_product)
        db.session.commit()

        items.append({'product_id': reserved_product.product_id, 'shopping_cart_id': reserved_product.shopping_cart_id})

    return items


def rent_product(product_id, user_id):
    reserved_product = db.session.query(ReservedProductRent).filter_by(user_id=user_id) \
        .filter_by(product_id=product_id).first()

    db.session.delete(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'user_id': reserved_product.user_id}


def get_price_for_product_buy(product_id):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    if product.discountValid:
        if product.discountValid > datetime.now().date():
            return {'product_name':product.name,
                    'product_price': product.price - (product.price / 100 * product.discountPercentage)}

    return {'product_name': product.name, 'product_price': product.price}


def get_price_for_product_rent(product_id):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    if product.discountValid:
        if product.discountValid > datetime.now().date():
            return {'product_name':product.name,
                    'product_price': product.price - (product.price / 100 * product.discountPercentage)}

    return {'product_name': product.name, 'product_price': product.price}


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
