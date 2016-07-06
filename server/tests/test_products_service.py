import unittest
from json import loads
import server.tests.utils as utils
import server.services.users as user_service
import server.services.products as product_service
from server.exceptions import AuthenticationException


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(GetProductsTestCase('test_get_products_success'))
    test_suite.addTest(GetProductsTestCase('test_get_products_invalid_token'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class GetProductsTestCase(unittest.TestCase):
    """Tests for `services/products.py - get_products()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_products_success(self):
        """With correct values, are valid products returned?"""

        # Get products
        products = product_service.get_products(self.loopback_token)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        products_json = loads(products)
        # Check that the products are valid
        for product_json in products_json:
            self.assertTrue(product_json.get('id'))
            self.assertTrue(product_json.get('name'))
            self.assertTrue(product_json.get('supplierId'))

    def test_get_products_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Attempt to get products with invalid token
        self.assertRaises(AuthenticationException,
                          product_service.get_products,
                          utils.get_bad_token())

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))

if __name__ == '__main__':
    unittest.main()
