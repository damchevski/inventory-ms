from socket import socket

import connexion
from consul import Check, Consul
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from schemas import *
import requests
from flask import request, abort
from functools import wraps
import jwt

consul_host = "consul"
consul_port = 8500
service_name = "inventory"
service_port = 5005

JWT_SECRET = "MY SECRET"

def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])


def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'AUTHORIZATION' in headers:
                    token = headers['AUTHORIZATION'].split(' ')[1]
                    decoded_token = decode_token(token)
                    if 'admin' in decoded_token['roles']:
                        return fn(*args, **kwargs)
                    for role in arg:
                        if role in decoded_token['roles']:
                            return fn(*args, **kwargs)
                    abort(401)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)

        return decorated_view

    return has_role_inner


@has_role(["admin"])
def create_coupon(coupon_body):
    coupon = Coupon(type=coupon_body['type'], quantity=coupon_body['quantity'])
    db.session.add(coupon)
    db.session.commit()

    return {'id':coupon.id, 'quantity':coupon.quantity}


@has_role(["admin"])
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


@has_role(["admin"])
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


@has_role(["admin"])
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


@has_role(["admin"])
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


@has_role(["admin"])
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


@has_role(["admin"])
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

@has_role(["admin"])
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


@has_role(["admin"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
def buy_coupon(coupon_id):
    coupon = db.session.query(Coupon).filter_by(id=coupon_id).first()

    if not coupon:
        return {'error': '{ not found'.format(coupon_id)}, 404

    coupon.quantity = coupon.quantity - 1

    db.session.commit()

    return {'id': coupon.id}


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
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


@has_role(["admin", "user"])
def buy_product(shopping_cart_id):
    reserved_products = db.session.query(ReservedProductBuy).filter_by(shopping_cart_id=shopping_cart_id).all()

    items = []
    for reserved_product in reserved_products:
        db.session.delete(reserved_product)
        db.session.commit()

        items.append({'product_id': reserved_product.product_id, 'shopping_cart_id': reserved_product.shopping_cart_id})

    return items


@has_role(["admin", "user"])
def rent_product(product_id, user_id):
    reserved_product = db.session.query(ReservedProductRent).filter_by(user_id=user_id) \
        .filter_by(product_id=product_id).first()

    db.session.delete(reserved_product)
    db.session.commit()

    return {'product_id': reserved_product.product_id, 'user_id': reserved_product.user_id}


@has_role(["admin", "user"])
def get_price_for_product_buy(product_id):
    product = db.session.query(ProductBuy).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    if product.discountValid:
        if product.discountValid > datetime.now().date():
            return {'product_name': product.name,
                    'product_price': product.price - (product.price / 100 * product.discountPercentage)}

    return {'product_name': product.name, 'product_price': product.price}


@has_role(["admin","user"])
def get_price_for_product_rent(product_id):
    product = db.session.query(ProductRent).filter_by(id=product_id).first()

    if not product:
        return {'error': '{} not found'.format(product_id)}, 404

    if product.discountValid:
        if product.discountValid > datetime.now().date():
            return {'product_name': product.name,
                    'product_price': product.price - (product.price / 100 * product.discountPercentage)}

    return {'product_name': product.name, 'product_price': product.price}


@has_role(["admin","user"])
def get_all_product_valid_discounts():
    products_buy = db.session.query(ProductBuy).all()
    products_rent = db.session.query(ProductRent).all()

    return_list = []

    for product in products_buy:
        if product.discountValid is not None:
            return_list.append({'product_id': product.id, 'product_type': 'buy',
                                'discount_valid_until': product.discountValid,
                                'discount_percentage': product.discountPercentage})

    for product in products_rent:
        if product.discountValid is not None:
            return_list.append({'product_id': product.id, 'product_type': 'rent',
                                'discount_valid_until': product.discountValid,
                                'discount_percentage': product.discountPercentage})

    return return_list


def get_host_name_IP():
    host_name_ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_name_ip = s.getsockname()[0]
        s.close()
        # print ("Host ip:", host_name_ip)
        return host_name_ip
    except:
        print("Unable to get Hostname")


def register_to_consul():
    consul = Consul(host="consul", port=consul_port)
    agent = consul.agent
    service = agent.service
    ip = get_host_name_IP()
    # print(ip)
    check = Check.http(f"http://{ip}:{service_port}/api/ui", interval="10s", timeout="5s", deregister="1s")
    service.register(service_name, service_id=service_name, address=ip, port=service_port, check=check)

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
