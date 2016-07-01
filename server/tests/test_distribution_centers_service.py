import unittest
from datetime import datetime
from json import loads
import server.services.demos as demo_service
import server.services.users as user_service
import server.services.distribution_centers as distribution_center_service
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

class GetDistributionCentersTestCase(unittest.TestCase):
    """Tests for `services/distribution_centers.py - get_distribution_centers()`."""

    def test_get_distribution_centers_success(self):
        """With correct values, are valid distribution centers returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get distribution centers
        distribution_centers = distribution_center_service.get_distribution_centers(loopback_token)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_distribution_centers_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Retrieve shipments with bad token
        bad_token = get_bad_token()

        # Attempt to get shipments with invalid token
        self.assertRaises(AuthenticationException,
                          distribution_center_service.get_distribution_centers,
                          bad_token)


class GetDistributionCenterTestCase(unittest.TestCase):
    """Tests for `services/distribution_centers.py - get_distribution_center()`."""

    def test_get_distribution_center_success(self):
        """With correct values, is a valid distribution center returned?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get distribution center
        distribution_centers = distribution_center_service.get_distribution_centers(loopback_token)
        dc_id = loads(distribution_centers)[0].get('id')
        distribution_center = distribution_center_service.get_distribution_center(loopback_token, dc_id)

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

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_distribution_center_invalid_input(self):
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Invalid distribution center id
        self.assertRaises(ResourceDoesNotExistException,
                          distribution_center_service.get_distribution_center,
                          loopback_token, '123321')

        # Destroy demo
        delete_demo(demo_guid)

    def test_get_distribution_center_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Get distribution centers
        distribution_centers = distribution_center_service.get_distribution_centers(loopback_token)
        dc_id = loads(distribution_centers)[0].get('id')

        # Retrieve distribution center with bad token
        bad_token = get_bad_token()

        # Attempt to get a distribution center with invalid token
        self.assertRaises(AuthenticationException,
                          distribution_center_service.get_distribution_center,
                          bad_token, dc_id)

        # Destroy demo
        delete_demo(demo_guid)

if __name__ == '__main__':
    unittest.main()
