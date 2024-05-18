import unittest
from app import create_app, db
from app.models import User, Product, Order
from config import TestingConfig

unittest.TestLoader.sortTestMethodsUsing = None

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        testApp = create_app(TestingConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class UserModelUnitTests(BaseTestCase):
    def test_password_hashing(self):
        user = User(username='yxlok', email_address='admin@mail.com')
        user.set_password('ecohub')
        self.assertFalse(user.check_password('ecohub123'))
        self.assertTrue(user.check_password('ecohub'))

    def test_user_creation(self):
        user = User(id=1, username='lokyx', first_name='yx', last_name='lok', is_seller=True, email_address='lokyx@example.com', password_hash='ecohub', postcode=6000, shop_name='my shop')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, 'lokyx')
        self.assertEqual(user.email_address, 'lokyx@example.com')
    
    def test_get_by_username(self):
        self.test_user_creation()
        fetched_user = User.get_by_username('lokyx')
        self.assertEqual(fetched_user.username, 'lokyx')

    def test_get_by_email(self):
        self.test_user_creation()
        fetched_user = User.get_by_email('lokyx@example.com')
        self.assertEqual(fetched_user.email_address, 'lokyx@example.com')

class ProductModelUnitTests(BaseTestCase):
    def test_product_creation(self):
        user = User(id=1, username='lokyx', first_name='yx', last_name='lok', is_seller=True, email_address='lokyx@example.com', password_hash='ecohub', postcode=6000, shop_name='my shop')
        product = Product(id=1, product_name='Product 1', category='Home & Garden', price=12.0, quantity=100, condition='Brand New', location=6000, description='Description 1', is_active=True)
        product.user_id= user.id
        db.session.add(product)
        db.session.commit()
        self.assertEqual(product.product_name, 'Product 1')
        self.assertEqual(product.category, 'Home & Garden')

    def test_get_by_id(self):
        self.test_product_creation()
        fetched_product = Product.get_by_id(1)
        self.assertEqual(fetched_product.product_name, 'Product 1')
        self.assertEqual(fetched_product.id, 1)
        self.assertEqual(fetched_product.user_id, 1)

    def test_activation_when_product_not_found(self):
        self.test_product_creation()
        product_id = 10
        user_id = 2
        result = Product.activation(product_id, user_id)
        self.assertIn('Product not found.', result['message'])
        self.assertFalse(result['success'])

    def test_activation_when_not_user_product(self):
        self.test_product_creation()
        product_id = 1
        user_id = 2
        result = Product.activation(product_id, user_id)
        self.assertIn('This is not your product.', result['message'])
        self.assertFalse(result['success'])

    def test_activation_when_success(self):
        self.test_product_creation()
        product_id = 1
        user_id = 1
        result = Product.activation(product_id, user_id)
        self.assertIn('Success', result['message'])
        self.assertTrue(result['success'])

class OrderModelUnitTests(BaseTestCase):
    def test_order_creation(self):
        user = User(id=1, username='lokyx', first_name='yx', last_name='lok', is_seller=True, email_address='lokyx@example.com', password_hash='ecohub', postcode=6000, shop_name='my shop')
        user2 = User(id=2, username='lwb', first_name='wb', last_name='l', is_seller=True, email_address='lwb@example.com', password_hash='ecohub2', postcode=6001, shop_name='lwb shop')
        product = Product(id=1, product_name='Product 1', category='Home & Garden', price=12.0, quantity=100, condition='Brand New', location=6000, description='Description 1', is_active=True)
        product.user_id= user.id
        order = Order(id=1, quantity=5, first_name='jy', last_name='y', email_address='yjy@example.com', postcode=6003, status="Pending")
        order.product_id = product.id
        order.buyer_id = user2.id
        db.session.add(product)
        db.session.add(order)
        db.session.commit()
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.last_name, 'y')

    def test_get_by_id(self):
        self.test_order_creation()
        fetched_order = Order.get_by_id(1)
        self.assertEqual(fetched_order.id, 1)
        self.assertEqual(fetched_order.product_id, 1)
        self.assertEqual(fetched_order.buyer_id, 2)

    def test_set_pending_status_when_order_not_found(self):
        self.test_order_creation()
        order_id = 2
        seller_id = 2
        status_to_update = "Success"
        result = Order.set_pending_status(order_id, seller_id, status_to_update)
        self.assertIn('Order not found.', result['message'])
        self.assertFalse(result['success'])

    def test_set_pending_status_when_order_not_in_pending(self):
        self.test_order_creation()

        order = Order.query.get(1)
        self.assertIsNotNone(order)

        order.status = "Approved"
        db.session.commit()
        
        order_id = 1
        seller_id = 2
        status_to_update = "Success"
        result = Order.set_pending_status(order_id, seller_id, status_to_update)
        self.assertIn('Order not in pending status.', result['message'])
        self.assertFalse(result['success'])

    def test_set_pending_status_when_product_not_found(self):
        self.test_order_creation()
        order_id = 1
        seller_id = 2
        status_to_update = "Success"

        product = Product.query.get(1)
        self.assertIsNotNone(product)
        product.id = 2
        db.session.commit()

        result = Order.set_pending_status(order_id, seller_id, status_to_update)
        self.assertIn('Product not found.', result['message'])
        self.assertFalse(result['success'])

    def test_set_pending_status_when_product_not_active(self):
        self.test_order_creation()
        order_id = 1
        seller_id = 2
        status_to_update = "Success"

        product = Product.query.get(1)
        self.assertIsNotNone(product)
        product.is_active = False
        db.session.commit()

        result = Order.set_pending_status(order_id, seller_id, status_to_update)
        self.assertIn('Product is not active.', result['message'])
        self.assertFalse(result['success'])

    def test_set_pending_status_when_not_seller_id(self):
        self.test_order_creation()
        order_id = 1
        seller_id = 2
        status_to_update = "Success"

        product = Product.query.get(1)
        self.assertIsNotNone(product)
        product.user_id = 10
        db.session.commit()

        result = Order.set_pending_status(order_id, seller_id, status_to_update)
        self.assertIn('This is not your product.', result['message'])
        self.assertFalse(result['success'])

    def test_set_pending_status_when_success(self):
        self.test_order_creation()
        order_id = 1
        seller_id = 1
        status_to_update = "Success"
        result = Order.set_pending_status(order_id, seller_id, status_to_update)
        self.assertIn(f'{status_to_update} the order.', result['message'])
        self.assertTrue(result['success'])

    def test_set_pending_status_when_success_and_update_qty(self):
        self.test_order_creation()
        order_id = 1
        seller_id = 1
        status_to_update = "Success"
        current_product_qty = Product.query.get(1).quantity
        order_qty = Order.query.get(1).quantity
        result = Order.set_pending_status(order_id, seller_id, status_to_update, update_qty=True)
        self.assertIn(f'{status_to_update} the order.', result['message'])
        self.assertTrue(result['success'])

        updated_product_qty = Product.query.get(1).quantity
        self.assertNotEqual(current_product_qty, updated_product_qty)
        self.assertEqual(current_product_qty-order_qty, updated_product_qty)

if __name__ == '__main__':
    unittest.main(verbosity=1)