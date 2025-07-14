from myclinic import create_app, db
from myclinic.models import Product, Order, OrderDetail

def run_seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        products = [
            Product(
                title='Starter Printable Kit',
                description='Essential digital forms and guides to launch your clinic.',
                price=29.99,
                image_filename='starter-printable-kit.jpg',
                slug='starter-printable-kit',
                stock=10,
                features="Intake forms,Patient guide,Checklist"
            ),
            Product(
                title='Branded Office Supplies',
                description='Complete package with custom branding and admin essentials.',
                price=79.99,
                image_filename='branded-office-supplies.jpg',
                slug='branded-office-supplies',
                stock=5,
                features="Appointment cards,Custom notepads,Branded pens"
            ),
            Product(
                title='Medical Supplies Kit',
                description='All-in-one kit includes key items to get your clinic started.',
                price=199.99,
                image_filename='medical-supplies-kit.jpg',
                slug='medical-supplies-kit',
                stock=3,
                features="Gloves,Masks,Bandages"
            )
        ]
        db.session.add_all(products)
        db.session.commit()
        print(f"Seeded {len(products)} products")

if __name__ == '__main__':
    run_seed()
