import unittest
from datetime import datetime
from json import loads
import server.services.demos as demo_service
import server.services.users as user_service
import server.services.retailers as retailer_service
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

class GetRetailersTestCase(unittest.TestCase):
    """Tests for `services/retailers.py - get_retailers()`."""

    def test_retailers_success(self):
        """With correct values, are valid retailers returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get retailers
        retailers = retailer_service.get_retailers(loopback_token)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_retailers_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Retrieve retailers with bad token
        bad_token = get_bad_token()

        # Attempt to get shipments with invalid token
        self.assertRaises(AuthenticationException,
                          retailer_service.get_retailers,
                          bad_token)


class GetRetailerTestCase(unittest.TestCase):
    """Tests for `services/retailers.py - get_retailers()`."""

    def test_get_retailer_success(self):
        """With correct values, is a valid distribution center returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get retailer
        retailers = retailer_service.get_retailers(loopback_token)
        retailer_id = loads(retailers)[0].get('id')
        retailer = retailer_service.get_retailer(loopback_token, retailer_id)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_retailer_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Invalid retailer id
        self.assertRaises(ResourceDoesNotExistException,
                          retailer_service.get_retailer,
                          loopback_token, 'R1-123')

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_retailer_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get retailers
        retailers = retailer_service.get_retailers(loopback_token)
        retailer_id = loads(retailers)[0].get('id')

        # Retrieve retailer with bad token
        bad_token = get_bad_token()

        # Attempt to get a distribution center with invalid token
        self.assertRaises(AuthenticationException,
                          retailer_service.get_retailer,
                          bad_token, retailer_id)

        # Destroy demo
        delete_demo(demo_guid)

if __name__ == '__main__':
    unittest.main()
