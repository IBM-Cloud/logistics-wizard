import unittest
from datetime import datetime
from json import loads
import server.services.demos as demo_service
from server.exceptions import (ValidationException,
                               UnprocessableEntityException,
                               ResourceDoesNotExistException)


###########################
#        Unit Tests       #
###########################

class CreateDemoTestCase(unittest.TestCase):
    """Tests for `services/demos.py - create_demo()`."""

    def test_demo_create_success(self):
        """With correct values, is a valid demo returned?"""

        # Create demo
        demo_name = datetime.now().isoformat("T")
        demo = demo_service.create_demo(demo_name)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        demo_json = loads(demo)
        self.assertTrue(demo_json.get('id'))
        self.assertTrue(demo_json.get('guid'))
        self.assertTrue(demo_json.get('name') == demo_name)
        self.assertTrue(demo_json.get('createdAt'))
        self.assertTrue(demo_json.get('users'))

        # Check that the default supplychainmanager user was created
        created_user_json = demo_json.get('users')[0]
        self.assertTrue(created_user_json.get('id'))
        self.assertTrue(created_user_json.get('demoId'))
        self.assertTrue(created_user_json.get('username'))
        self.assertTrue(created_user_json.get('email'))
        self.assertTrue(created_user_json.get('roles'))

        # Check that the proper role was created
        scm_role_json = created_user_json.get('roles')[0]
        self.assertTrue(scm_role_json.get('id'))
        self.assertTrue(scm_role_json.get('name') == "supplychainmanager")
        self.assertTrue(scm_role_json.get('created'))
        self.assertTrue(scm_role_json.get('modified'))

        # Destroy demo
        demo_service.delete_demo_by_guid(demo_json.get('guid'))

    def test_demo_create_email(self):
        """Is an invalid email detected correctly?"""

        # Test invalid email throws ValidationException
        demo_name = datetime.now().isoformat("T")
        invalid_email = "email@example@example.com"
        self.assertRaises(UnprocessableEntityException,
                          demo_service.create_demo,
                          demo_name, invalid_email)

        # Test valid email completes
        demo_name = datetime.now().isoformat("T")
        invalid_email = "firstname-lastname@example.com"
        demo = demo_service.create_demo(demo_name, invalid_email)
        self.assertTrue(loads(demo).get('id'))


class RetrieveDemoTestCase(unittest.TestCase):
    """Tests for `services/demos.py - get_demo_by_guid()`."""

    def test_demo_retrieve_success(self):
        """With correct values, is a valid demo returned?"""

        # Create and then retrieve demo
        demo_name = datetime.now().isoformat("T")
        created_demo = demo_service.create_demo(demo_name)
        retrieved_demo = demo_service.get_demo_by_guid(loads(created_demo).get('guid'))

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        demo_json = loads(retrieved_demo)
        self.assertTrue(demo_json.get('id') == loads(created_demo).get('id'))
        self.assertTrue(demo_json.get('guid') == loads(created_demo).get('guid'))
        self.assertTrue(demo_json.get('name') == loads(created_demo).get('name'))
        self.assertTrue(demo_json.get('createdAt') == loads(created_demo).get('createdAt'))
        self.assertTrue(demo_json.get('users'))

        # Check that the users are valid
        for user_json in demo_json.get('users'):
            self.assertTrue(user_json.get('id'))
            self.assertTrue(user_json.get('demoId'))
            self.assertTrue(user_json.get('username'))
            self.assertTrue(user_json.get('email'))

            # Check that user roles are valid, if present
            if user_json.get('roles'):
                for role_json in user_json.get('roles'):
                    self.assertTrue(role_json.get('id'))
                    self.assertTrue(role_json.get('name'))
                    self.assertTrue(role_json.get('created'))
                    self.assertTrue(role_json.get('modified'))

        # Destroy demo
        demo_service.delete_demo_by_guid(demo_json.get('guid'))

    def test_demo_retrieve_invalid_inputs(self):
        """With an invalid inputs, are correct errors thrown?"""

        # Attempt to create demo with invalid guid
        self.assertRaises(ResourceDoesNotExistException,
                          demo_service.get_demo_by_guid,
                          'ABC123')

if __name__ == '__main__':
    unittest.main()
