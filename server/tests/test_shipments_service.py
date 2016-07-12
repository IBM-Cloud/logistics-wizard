import unittest
from json import loads
import server.tests.utils as utils
import server.services.users as user_service
import server.services.shipments as shipment_service
import server.services.retailers as retailer_service
import server.services.distribution_centers as distribution_center_service
from server.exceptions import (AuthenticationException,
                               ResourceDoesNotExistException,
                               UnprocessableEntityException)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(GetShipmentsTestCase('test_get_shipments_success'))
    test_suite.addTest(GetShipmentsTestCase('test_get_shipments_status_filter_success'))
    test_suite.addTest(GetShipmentsTestCase('test_get_shipments_retailer_id_filter_success'))
    test_suite.addTest(GetShipmentsTestCase('test_get_shipments_invalid_token'))
    test_suite.addTest(CreateShipmentTestCase('test_create_shipment_success'))
    test_suite.addTest(CreateShipmentTestCase('test_create_shipment_invalid_ids'))
    test_suite.addTest(CreateShipmentTestCase('test_create_shipment_invalid_token'))
    test_suite.addTest(GetShipmentTestCase('test_get_shipment_success'))
    test_suite.addTest(GetShipmentTestCase('test_get_shipment_invalid_input'))
    test_suite.addTest(GetShipmentTestCase('test_get_shipment_invalid_token'))
    test_suite.addTest(DeleteShipmentTestCase('test_delete_shipment_success'))
    test_suite.addTest(DeleteShipmentTestCase('test_delete_shipment_invalid_input'))
    test_suite.addTest(DeleteShipmentTestCase('test_delete_shipment_invalid_token'))
    test_suite.addTest(UpdateShipmentTestCase('test_update_shipment_success'))
    test_suite.addTest(UpdateShipmentTestCase('test_update_shipment_invalid_input'))
    test_suite.addTest(UpdateShipmentTestCase('test_update_shipment_invalid_token'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class GetShipmentsTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - get_shipments()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_shipments_success(self):
        """With correct values, are valid shipments returned?"""

        # Get shipments
        shipments = shipment_service.get_shipments(self.loopback_token)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipments_json = loads(shipments)
        # Check that the shipments are valid
        for shipment_json in shipments_json:
            self.assertTrue(shipment_json.get('id'))
            self.assertTrue(shipment_json.get('status'))
            self.assertTrue(shipment_json.get('createdAt'))
            self.assertTrue(shipment_json.get('estimatedTimeOfArrival'))
            self.assertTrue(shipment_json.get('fromId'))
            self.assertTrue(shipment_json.get('toId'))

            # Check that shipment address is valid, if present
            if shipment_json.get('currentLocation'):
                self.assertTrue(shipment_json.get('currentLocation').get('city'))
                self.assertTrue(shipment_json.get('currentLocation').get('state'))
                self.assertTrue(shipment_json.get('currentLocation').get('country'))
                self.assertTrue(shipment_json.get('currentLocation').get('latitude'))
                self.assertTrue(shipment_json.get('currentLocation').get('longitude'))

    def test_get_shipments_status_filter_success(self):
        """Are correct status shipments returned?"""

        # Get shipments with specific status
        query_status = 'DELIVERED'
        shipments = shipment_service.get_shipments(self.loopback_token, status=query_status)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipments_json = loads(shipments)
        # Check that the shipments have correct status
        for shipment_json in shipments_json:
            self.assertTrue(shipment_json.get('status') == query_status)

    def test_get_shipments_retailer_id_filter_success(self):
        """Are correct retailers' shipments returned?"""

        # Get shipments intended for specific retailer
        retailers = retailer_service.get_retailers(self.loopback_token)
        retailer_id_filter = loads(retailers)[0].get('id')
        shipments = shipment_service.get_shipments(self.loopback_token, retailer_id=retailer_id_filter)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipments_json = loads(shipments)
        # Check that the shipments have correct retailer ID (toId)
        for shipment_json in shipments_json:
            self.assertTrue(shipment_json.get('toId') == retailer_id_filter)

    def test_get_shipments_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        self.assertRaises(AuthenticationException,
                          shipment_service.get_shipments,
                          utils.get_bad_token())

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class CreateShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - create_shipment()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_create_shipment_success(self):
        """With correct values, is a valid shipment created?"""

        # Get retailers and distribution centers
        retailers = retailer_service.get_retailers(self.loopback_token)
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)

        # Create shipment
        shipment = dict()
        shipment['fromId'] = loads(distribution_centers)[0].get('id')
        shipment['toId'] = loads(retailers)[0].get('id')
        shipment['estimatedTimeOfArrival'] = "2016-07-14"
        created_shipment = shipment_service.create_shipment(self.loopback_token, shipment)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipment_json = loads(created_shipment)
        # Check that the shipment is valid
        self.assertTrue(shipment_json.get('id'))
        self.assertTrue(shipment_json.get('status'))
        self.assertTrue(shipment_json.get('createdAt'))
        self.assertTrue(shipment_json.get('fromId'))
        self.assertTrue(shipment_json.get('toId'))

    def test_create_shipment_invalid_ids(self):
        """With an invalid retailer/distribution center IDs, are correct errors thrown?"""

        # Get retailers and distribution centers
        retailers = retailer_service.get_retailers(self.loopback_token)
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)

        # Create invalid shipments
        shipment_invalid_retailer = dict()
        shipment_invalid_retailer['fromId'] = loads(distribution_centers)[0].get('id')
        shipment_invalid_retailer['toId'] = "123321"
        shipment_invalid_dist = dict()
        shipment_invalid_dist['fromId'] = "123321"
        shipment_invalid_dist['toId'] = loads(retailers)[0].get('id')

        # Attempt to create a shipment with invalid IDs
        self.assertRaises(UnprocessableEntityException,
                          shipment_service.create_shipment,
                          self.loopback_token, shipment_invalid_retailer)
        self.assertRaises(UnprocessableEntityException,
                          shipment_service.create_shipment,
                          self.loopback_token, shipment_invalid_dist)

    def test_create_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get retailers and distribution centers
        retailers = retailer_service.get_retailers(self.loopback_token)
        distribution_centers = distribution_center_service.get_distribution_centers(self.loopback_token)

        # Create shipment
        shipment = dict()
        shipment['fromId'] = loads(distribution_centers)[0].get('id')
        shipment['toId'] = loads(retailers)[0].get('id')
        shipment['estimatedTimeOfArrival'] = "2016-07-14"
        created_shipment = shipment_service.create_shipment(self.loopback_token, shipment)

        # Attempt to create a shipment with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.create_shipment,
                          utils.get_bad_token(), shipment)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class GetShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - get_shipment()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_get_shipment_success(self):
        """With correct values, is a valid shipment returned?"""

        # Get a shipment
        shipments = shipment_service.get_shipments(self.loopback_token)
        shipment_id = loads(shipments)[0].get('id')
        shipment = shipment_service.get_shipment(self.loopback_token, shipment_id)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipment_json = loads(shipment)
        # Check that the shipment is valid
        self.assertTrue(shipment_json.get('id'))
        self.assertTrue(shipment_json.get('status'))
        self.assertTrue(shipment_json.get('createdAt'))
        self.assertTrue(shipment_json.get('estimatedTimeOfArrival'))
        self.assertTrue(shipment_json.get('fromId'))
        self.assertTrue(shipment_json.get('toId'))

        # Check that shipment address is valid, if present
        if shipment_json.get('currentLocation'):
            self.assertTrue(shipment_json.get('currentLocation').get('city'))
            self.assertTrue(shipment_json.get('currentLocation').get('state'))
            self.assertTrue(shipment_json.get('currentLocation').get('country'))
            self.assertTrue(shipment_json.get('currentLocation').get('latitude'))
            self.assertTrue(shipment_json.get('currentLocation').get('longitude'))

    def test_get_shipment_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        self.assertRaises(ResourceDoesNotExistException,
                          shipment_service.get_shipment,
                          self.loopback_token, '123321')

    def test_get_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get valid shipment ID
        shipments = shipment_service.get_shipments(self.loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Attempt to get a shipment with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.get_shipment,
                          utils.get_bad_token(), shipment_id)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class DeleteShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - delete_shipment()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_delete_shipment_success(self):
        """With correct values, is the shipment deleted?"""

        # Get a specific shipment
        shipments = shipment_service.get_shipments(self.loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Delete shipment and check for successful return
        self.assertTrue(shipment_service.delete_shipment(self.loopback_token, shipment_id) is None)

    def test_delete_shipment_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        self.assertRaises(ResourceDoesNotExistException,
                          shipment_service.delete_shipment,
                          self.loopback_token, '123321')

    def test_delete_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get a specific shipment ID
        shipments = shipment_service.get_shipments(self.loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Attempt to delete a shipment with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.delete_shipment,
                          utils.get_bad_token(), shipment_id)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))


class UpdateShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - update_shipment()`."""

    def setUp(self):
        # Create demo
        self.demo = utils.create_demo()
        demo_json = loads(self.demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        self.loopback_token = auth_data.get('loopback_token')

    def test_update_shipment_success(self):
        """With correct values, is the shipment updated?"""

        # Get a specific shipment
        shipments = shipment_service.get_shipments(self.loopback_token, status="NEW")
        shipment_id = loads(shipments)[0].get('id')

        # Change status of shipment
        new_status = 'APPROVED'
        shipment = dict()
        shipment['status'] = new_status
        updated_shipment = shipment_service.update_shipment(self.loopback_token, shipment_id, shipment)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipment_json = loads(updated_shipment)
        # Check that the shipments are valid
        self.assertTrue(shipment_json.get('id'))
        self.assertTrue(shipment_json.get('status') == new_status)
        self.assertTrue(shipment_json.get('createdAt'))
        self.assertTrue(shipment_json.get('estimatedTimeOfArrival'))
        self.assertTrue(shipment_json.get('fromId'))
        self.assertTrue(shipment_json.get('toId'))

        # Check that shipment address is valid, if present
        if shipment_json.get('currentLocation'):
            self.assertTrue(shipment_json.get('currentLocation').get('city'))
            self.assertTrue(shipment_json.get('currentLocation').get('state'))
            self.assertTrue(shipment_json.get('currentLocation').get('country'))
            self.assertTrue(shipment_json.get('currentLocation').get('latitude'))
            self.assertTrue(shipment_json.get('currentLocation').get('longitude'))

    def test_update_shipment_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        # Invalid shipment id
        shipment = dict()
        shipment['status'] = 'ACCEPTED'
        self.assertRaises(ResourceDoesNotExistException,
                          shipment_service.update_shipment,
                          self.loopback_token, '123321', shipment)

    def test_update_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Get a specific shipment ID
        shipments = shipment_service.get_shipments(self.loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Attempt to delete a shipment with invalid token
        shipment = dict()
        shipment['status'] = 'ACCEPTED'
        self.assertRaises(AuthenticationException,
                          shipment_service.update_shipment,
                          utils.get_bad_token(), shipment_id, shipment)

    def tearDown(self):
        utils.delete_demo(loads(self.demo).get('guid'))

if __name__ == '__main__':
    unittest.main()
