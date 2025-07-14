from myclinic import db  
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,    nullable=False)
    price       = db.Column(db.Float,   nullable=False)
    image_filename  = db.Column(db.String(255), nullable=True) 
    slug        = db.Column(db.String(100), unique=True, nullable=False)
    stock       = db.Column(db.Integer, default=0)
    features       = db.Column(db.Text,      nullable=True)


    order_items = db.relationship(
        'OrderDetail',
        back_populates='product',
        cascade='all, delete-orphan'
    )

class Order(db.Model):
    __tablename__ = 'orders'

    id           = db.Column(db.Integer, primary_key=True)
    customer     = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(120), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status       = db.Column(db.String(20), default='pending', nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    items = db.relationship(
        'OrderDetail',
        back_populates='order',
        cascade='all, delete-orphan'
    )

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'),   nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    order   = db.relationship('Order',   back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    
