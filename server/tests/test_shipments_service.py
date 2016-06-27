import unittest
from datetime import datetime
from json import loads, dumps
import server.services.demos as demo_service
import server.services.users as user_service
import server.services.shipments as shipment_service
import server.services.retailers as retailer_service
from server.exceptions import (ValidationException,
                               AuthenticationException,
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

class GetShipmentsTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - get_shipments()`."""

    def test_get_shipments_success(self):
        """With correct values, are valid shipments returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_shipments_status_filter_success(self):
        """Are correct status shipments returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        query_status = 'SHIPPED'
        shipments = shipment_service.get_shipments(loopback_token, status=query_status)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipments_json = loads(shipments)
        # Check that the shipments have correct status
        for shipment_json in shipments_json:
            self.assertTrue(shipment_json.get('status') == query_status)

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_shipments_retailer_id_filter_success(self):
        """Are correct retailers' shipments returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        retailers = retailer_service.get_retailers(loopback_token)
        retailer_id = loads(retailers)[0].get('id')
        shipments = shipment_service.get_shipments(loopback_token, retailer_id=retailer_id)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipments_json = loads(shipments)
        # Check that the shipments have correct retailer ID (toId)
        for shipment_json in shipments_json:
            self.assertTrue(shipment_json.get('toId') == retailer_id)

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_shipments_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Retrieve shipments with bad token
        bad_token = get_bad_token()

        # Attempt to get shipments with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.get_shipments,
                          bad_token)


class CreateShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - create_shipment()`."""

    def test_create_shipment_success(self):
        """With correct values, is a valid shipment created?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        from_id = loads(shipments)[0].get('fromId')
        to_id = loads(shipments)[0].get('toId')

        # Create shipment
        shipment = dict()
        shipment['fromId'] = from_id
        shipment['toId'] = to_id
        created_shipment = shipment_service.create_shipment(loopback_token, shipment)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        shipment_json = loads(created_shipment)
        # Check that the shipment is valid
        self.assertTrue(shipment_json.get('id'))
        self.assertTrue(shipment_json.get('status'))
        self.assertTrue(shipment_json.get('createdAt'))
        self.assertTrue(shipment_json.get('fromId'))
        self.assertTrue(shipment_json.get('toId'))

        # Destroy demo
        delete_demo(demo_guid)

    def test_create_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        from_id = loads(shipments)[0].get('fromId')
        to_id = loads(shipments)[0].get('toId')

        # Create shipment
        shipment = dict()
        shipment['fromId'] = from_id
        shipment['toId'] = to_id

        # Retrieve shipment with bad token
        bad_token = get_bad_token()

        # Attempt to create a shipment with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.create_shipment,
                          bad_token, shipment)

        # Destroy demo
        delete_demo(demo_guid)


class GetShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - get_shipment()`."""

    def test_get_shipment_success(self):
        """With correct values, is a valid shipment returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        shipment_id = loads(shipments)[0].get('id')
        shipment = shipment_service.get_shipment(loopback_token, shipment_id)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_shipment_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Invalid shipment id
        self.assertRaises(ResourceDoesNotExistException,
                          shipment_service.get_shipment,
                          loopback_token, 'S1-123')

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Retrieve shipment with bad token
        bad_token = get_bad_token()

        # Attempt to get a shipment with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.get_shipment,
                          bad_token, shipment_id)

        # Destroy demo
        delete_demo(demo_guid)


class DeleteShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - delete_shipment()`."""

    def test_delete_shipment_success(self):
        """With correct values, is the shipment deleted?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Delete shipment and check for successful return
        self.assertTrue(shipment_service.delete_shipment(loopback_token, shipment_id) is None)

        # Destroy demo
        delete_demo(demo_guid)

    def test_delete_shipment_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Invalid shipment id
        self.assertRaises(ResourceDoesNotExistException,
                          shipment_service.delete_shipment,
                          loopback_token, 'S1-123')

        # Destroy demo
        delete_demo(demo_guid)

    def test_delete_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Delete shipment with bad token
        bad_token = get_bad_token()

        # Attempt to delete a shipment with invalid token
        self.assertRaises(AuthenticationException,
                          shipment_service.delete_shipment,
                          bad_token, shipment_id)

        # Destroy demo
        delete_demo(demo_guid)


class UpdateShipmentTestCase(unittest.TestCase):
    """Tests for `services/shipments.py - update_shipment()`."""

    def test_update_shipment_success(self):
        """With correct values, is the shipment updated?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        shipment_id = loads(shipments)[0].get('id')
        shipment = shipment_service.get_shipment(loopback_token, shipment_id)

        # Change status of shipment
        new_status = 'ACCEPTED'
        shipment = dict()
        shipment['status'] = new_status
        updated_shipment = shipment_service.update_shipment(loopback_token, shipment_id, shipment)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_update_shipment_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Invalid shipment id
        shipment = dict()
        shipment['status'] = 'ACCEPTED'
        self.assertRaises(ResourceDoesNotExistException,
                          shipment_service.update_shipment,
                          loopback_token, 'S1-123', shipment)

        # Destroy demo
        delete_demo(demo_guid)

    def test_update_shipment_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get shipments
        shipments = shipment_service.get_shipments(loopback_token)
        shipment_id = loads(shipments)[0].get('id')

        # Update shipment with bad token
        bad_token = get_bad_token()

        # Attempt to delete a shipment with invalid token
        shipment = dict()
        shipment['status'] = 'ACCEPTED'
        self.assertRaises(AuthenticationException,
                          shipment_service.update_shipment,
                          bad_token, shipment_id, shipment)

        # Destroy demo
        delete_demo(demo_guid)

if __name__ == '__main__':
    unittest.main()
