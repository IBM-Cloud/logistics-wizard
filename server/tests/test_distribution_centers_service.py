import unittest
from json import loads
from types import IntType
import server.tests.utils as utils
import server.services.users as user_service
import server.services.distribution_centers as distribution_center_service
from server.exceptions import (AuthenticationException,
                               ResourceDoesNotExistException)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(GetDistributionCentersTestCase('test_get_distribution_centers_success'))
    test_suite.addTest(GetDistributionCentersTestCase('test_get_distribution_centers_invalid_token'))
    test_suite.addTest(GetDistributionCenterTestCase('test_get_distribution_center_success'))
    test_suite.addTest(GetDistributionCenterTestCase('test_get_distribution_center_invalid_input'))
    test_suite.addTest(GetDistributionCenterTestCase('test_get_distribution_center_invalid_token'))
    test_suite.addTest(GetDistributionCenterInventoryTestCase('test_get_distribution_center_inventory_success'))
    test_suite.addTest(GetDistributionCenterInventoryTestCase('test_get_distribution_center_inventory_invalid_input'))
    test_suite.addTest(GetDistributionCenterInventoryTestCase('test_get_distribution_center_inventory_invalid_token'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class GetDistributionCentersTestCase(unittest.TestCase):
    """Tests for `services/distribution_centers.py - get_distribution_centers()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_distribution_centers_success(self):
        """With correct values, are valid distribution centers returned?"""

        # Get distribution centers
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        distribution_centers_json = loads(distribution_centers)
        # Check that the distribution centers are valid
        for distribution_center_json in distribution_centers_json:
            self.assertTrue(distribution_center_json.get('id'))

            # Check that distribution center address is valid, if present
            if distribution_center_json.get('address'):
                self.assertTrue(distribution_center_json.get('address').get('city'))
                self.assertTrue(distribution_center_json.get('address').get('state'))
                self.assertTrue(distribution_center_json.get('address').get('country'))
                self.assertTrue(distribution_center_json.get('address').get('latitude'))
                self.assertTrue(distribution_center_json.get('address').get('longitude'))

            # Check that distribution center contact is valid, if present
            if distribution_center_json.get('contact'):
                self.assertTrue(distribution_center_json.get('contact').get('name'))

    def test_get_distribution_centers_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        self.assertRaises(AuthenticationException,
                          distribution_center_service.get_distribution_centers,
                          utils.get_bad_token())

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class GetDistributionCenterTestCase(unittest.TestCase):
    """Tests for `services/distribution_centers.py - get_distribution_center()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_distribution_center_success(self):
        """With correct values, is a valid distribution center returned?"""

        # Get distribution center
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)
        dc_id = loads(distribution_centers)[0].get('id')
        distribution_center = distribution_center_service.get_distribution_center(self.loopback_token, dc_id)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        distribution_center_json = loads(distribution_center)
        # Check that the distribution center is valid
        self.assertTrue(distribution_center_json.get('id'))

        # Check that distribution center address is valid, if present
        if distribution_center_json.get('address'):
            self.assertTrue(distribution_center_json.get('address').get('city'))
            self.assertTrue(distribution_center_json.get('address').get('state'))
            self.assertTrue(distribution_center_json.get('address').get('country'))
            self.assertTrue(distribution_center_json.get('address').get('latitude'))
            self.assertTrue(distribution_center_json.get('address').get('longitude'))

        # Check that distribution center contact is valid, if present
        if distribution_center_json.get('contact'):
            self.assertTrue(distribution_center_json.get('contact').get('name'))

    def test_get_distribution_center_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        self.assertRaises(ResourceDoesNotExistException,
                          distribution_center_service.get_distribution_center,
                          self.loopback_token, '123321')

    def test_get_distribution_center_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get distribution centers
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)
        dc_id = loads(distribution_centers)[0].get('id')

        # Attempt to get a distribution center with invalid token
        self.assertRaises(AuthenticationException,
                          distribution_center_service.get_distribution_center,
                          utils.get_bad_token(), dc_id)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class GetDistributionCenterInventoryTestCase(unittest.TestCase):
    """Tests for `services/distribution_centers.py - get_distribution_center_inventory()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_distribution_center_inventory_success(self):
        """With correct values, is valid inventory returned?"""

        # Get distribution center
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)
        dc_id = loads(distribution_centers)[0].get('id')
        inventory = distribution_center_service.get_distribution_center_inventory(self.loopback_token, dc_id)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        inventories_json = loads(inventory)
        for inventory_json in inventories_json:
            self.assertTrue(inventory_json.get('id'))
            self.assertIsInstance(inventory_json.get('quantity'), IntType)
            self.assertTrue(inventory_json.get('productId'))
            self.assertTrue(inventory_json.get('locationId'))
            self.assertTrue(inventory_json.get('locationType'))

    def test_get_distribution_center_inventory_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        self.assertRaises(ResourceDoesNotExistException,
                          distribution_center_service.get_distribution_center_inventory,
                          self.loopback_token, '123321')

    def test_get_distribution_center_inventory_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get distribution centers
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)
        dc_id = loads(distribution_centers)[0].get('id')

        # Attempt to get retailer inventory with invalid token
        self.assertRaises(AuthenticationException,
                          distribution_center_service.get_distribution_center_inventory,
                          utils.get_bad_token(), dc_id)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))

if __name__ == '__main__':
    unittest.main()
