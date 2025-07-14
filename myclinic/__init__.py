from flask import (
    Flask, render_template, abort,
    session, redirect, url_for,
    request, flash, get_flashed_messages
)
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='supersecret',
        SQLALCHEMY_DATABASE_URI='sqlite:///milton.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)
    )

    db.init_app(app)
    Bootstrap(app)

    from .models import Product, Order, OrderDetail

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.route('/')
    @app.route('/home')
    def home():
        products = Product.query.all()
        return render_template('index.html', products=products)

    @app.route('/cart')
    def cart():
        raw = session.get('cart', {})
        items, total = [], 0.0
        for key, qty in raw.items():
            pid = int(key)
            p = Product.query.get(pid)
            if not p:
                continue
            subtotal = p.price * qty
            items.append({
                'id':       pid,
                'title':    p.title,
                'price':    p.price,
                'qty':      qty,
                'subtotal': subtotal
            })
            total += subtotal
        return render_template('cart.html', items=items, total=total)

    @app.route('/add-to-cart/<int:product_id>')
    def add_to_cart(product_id):
        cart = session.get('cart', {})
        key = str(product_id)
        cart[key] = cart.get(key, 0) + 1
        session['cart'] = cart
        flash('Added to cart!', 'success')
        return redirect(url_for('cart'))

    @app.route('/remove-from-cart/<int:product_id>')
    def remove_from_cart(product_id):
        cart = session.get('cart', {})
        cart.pop(str(product_id), None)
        session['cart'] = cart
        flash('Removed from cart.', 'warning')
        return redirect(url_for('cart'))

    @app.route('/checkout', methods=['GET','POST'])
    def checkout():
        get_flashed_messages()
        cart_data = session.get('cart', {})
        if not cart_data:
            flash('Your cart is empty.', 'info')
            return redirect(url_for('cart'))

        total = sum(
            Product.query.get(pid).price * qty
            for pid, qty in cart_data.items()
            if Product.query.get(pid)
        )

        if request.method == 'POST':
            order = Order(
                customer=request.form['name'],
                email=request.form['email'],
                status='pending',
                total_amount=total
            )
            db.session.add(order)
            db.session.flush()

            for pid, qty in cart_data.items():
                p = Product.query.get(pid)
                if not p: continue
                db.session.add(OrderDetail(
                    order_id=order.id,
                    product_id=pid,
                    quantity=qty,
                    unit_price=p.price
                ))

            db.session.commit()
            session.pop('cart', None)
            
            return redirect(url_for('order', order_id=order.id))

        return render_template('checkout.html', total=total)

    @app.route('/order/<int:order_id>')
    def order(order_id):
        order = Order.query.get_or_404(order_id)
        return render_template('order.html', order=order)

    @app.route('/product/<slug>')
    def product_detail(slug):
        item = Product.query.filter_by(slug=slug).first_or_404()
        raw      = item.features or ""
        features = [f.strip() for f in raw.split(',') if f.strip()]
        similar  = (
            Product.query
                   .filter(Product.id != item.id)
                   .limit(2)
                   .all()
        )
        return render_template(
            'product_detail.html',
            item=item,
            features=features,
            similar=similar
        )

    @app.route('/500')
    def trigger_error():
        abort(500)

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app
