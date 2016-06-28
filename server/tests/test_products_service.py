import unittest
from datetime import datetime
from json import loads
import server.services.demos as demo_service
import server.services.users as user_service
import server.services.products as product_service
from server.exceptions import (AuthenticationException,
                               ResourceDoesNotExistException)


###########################
#        Utilities        #
###########################

def create_demo():
    """Creates a demo object to work with for the unit tests"""

    demo_name = datetime.now().isoformat("T")
    return demo_service.create_demo(demo_name)


def delete_demo(demo_guid):
    """Deletes the demo object used by the unit tests"""

    demo_service.delete_demo_by_guid(demo_guid)


def get_bad_token():
    """Returns an invalid loopback token"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJu" \
           "YW1lIjoiU3VwcGx5IENoYWluIE1hbmFnZXIgKG1kcTNRMEZDYlEpIiwiZ" \
           "GVtb0lkIjoiN2U3ZjQ1ZTA1ZTQyNTFiNWFjZDBiMTlmYTRlZDI5OTIiLC" \
           "JlbWFpbCI6ImNocmlzLm1kcTNRMEZDYlFAYWNtZS5jb20iLCJyb2xlcyI" \
           "6W3siY3JlYXRlZCI6IjIwMTYtMDYtMDFUMTE6MTU6MzQuNTE1WiIsImlk" \
           "IjoiM2RlZjE0MzZlYjUxZTQzOWU3ZmI1MDA5ZmVjM2EwZWIiLCJtb2RpZ" \
           "mllZCI6IjIwMTYtMDYtMDFUMTE6MTU6MzQuNTE1WiIsIm5hbWUiOiJzdX" \
           "BwbHljaGFpbm1hbmFnZXIifV0sImlkIjoiN2U3ZjQ1ZTA1ZTQyNTFiNWF" \
           "jZDBiMTlmYTRlZDQ3OTAifSwiZXhwIjoxNDY2MDQ1MzczLCJsb29wYmFj" \
           "a190b2tlbiI6ImhFRnJzeGhSa3lBUEhQWWN0TWtEaE9mSTZOaDY5TlBzc" \
           "FhkRWhxWXVSTzBqZDBLem1HVkZFbnpRZVRwVTV2N28ifQ.I8_iqpK7pwY" \
           "5mmND220MhnsMDS5FtqRhtliEiXoMAGM"


###########################
#        Unit Tests       #
###########################

class GetProductsTestCase(unittest.TestCase):
    """Tests for `services/products.py - get_products()`."""

    def test_get_products_success(self):
        """With correct values, are valid products returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get products
        products = product_service.get_products(loopback_token)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        products_json = loads(products)
        # Check that the products are valid
        for product_json in products_json:
            self.assertTrue(product_json.get('id'))
            self.assertTrue(product_json.get('name'))
            self.assertTrue(product_json.get('supplierId'))

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_products_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Retrieve products with bad token
        bad_token = get_bad_token()

        # Attempt to get products with invalid token
        self.assertRaises(AuthenticationException,
                          product_service.get_products,
                          bad_token)

if __name__ == '__main__':
    unittest.main()
