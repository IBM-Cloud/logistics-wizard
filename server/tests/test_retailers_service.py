import unittest
from json import loads
import server.tests.utils as utils
import server.services.users as user_service
import server.services.retailers as retailer_service
from server.exceptions import (AuthenticationException,
                               ResourceDoesNotExistException)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(GetRetailersTestCase('test_retailers_success'))
    test_suite.addTest(GetRetailersTestCase('test_get_retailers_invalid_token'))
    test_suite.addTest(GetRetailerTestCase('test_get_retailer_success'))
    test_suite.addTest(GetRetailerTestCase('test_get_retailer_invalid_input'))
    test_suite.addTest(GetRetailerTestCase('test_get_retailer_invalid_token'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class GetRetailersTestCase(unittest.TestCase):
    """Tests for `services/retailers.py - get_retailers()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_retailers_success(self):
        """With correct values, are valid retailers returned?"""

        # Get retailers
        retailers = retailer_service.get_retailers(self.loopback_token)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        retailers_json = loads(retailers)
        # Check that the retailers are valid
        for retailer_json in retailers_json:
            self.assertTrue(retailer_json.get('id'))

            # Check that retailer address is valid, if present
            if retailer_json.get('address'):
                self.assertTrue(retailer_json.get('address').get('city'))
                self.assertTrue(retailer_json.get('address').get('state'))
                self.assertTrue(retailer_json.get('address').get('country'))
                self.assertTrue(retailer_json.get('address').get('latitude'))
                self.assertTrue(retailer_json.get('address').get('longitude'))

    def test_get_retailers_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        self.assertRaises(AuthenticationException,
                          retailer_service.get_retailers,
                          utils.get_bad_token())

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class GetRetailerTestCase(unittest.TestCase):
    """Tests for `services/retailers.py - get_retailers()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_retailer_success(self):
        """With correct values, is a valid distribution center returned?"""

        # Get retailer
        retailers = retailer_service.get_retailers(self.loopback_token)
        retailer_id = loads(retailers)[0].get('id')
        retailer = retailer_service.get_retailer(self.loopback_token, retailer_id)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        retailer_json = loads(retailer)
        # Check that the retailer is valid
        self.assertTrue(retailer_json.get('id'))

        # Check that retailer address is valid, if present
        if retailer_json.get('address'):
            self.assertTrue(retailer_json.get('address').get('city'))
            self.assertTrue(retailer_json.get('address').get('state'))
            self.assertTrue(retailer_json.get('address').get('country'))
            self.assertTrue(retailer_json.get('address').get('latitude'))
            self.assertTrue(retailer_json.get('address').get('longitude'))

    def test_get_retailer_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        self.assertRaises(ResourceDoesNotExistException,
                          retailer_service.get_retailer,
                          self.loopback_token, '123321')

    def test_get_retailer_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get retailers
        retailers = retailer_service.get_retailers(self.loopback_token)
        retailer_id = loads(retailers)[0].get('id')

        # Attempt to get a distribution center with invalid token
        self.assertRaises(AuthenticationException,
                          retailer_service.get_retailer,
                          utils.get_bad_token(), retailer_id)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))

if __name__ == '__main__':
    unittest.main()
