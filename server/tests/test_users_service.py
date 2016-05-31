import unittest
from datetime import datetime
from json import loads
import server.services.demos as demo_service
import server.services.users as user_service
from server.exceptions import (ResourceDoesNotExistException)


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


###########################
#        Unit Tests       #
###########################

class CreateUserTestCase(unittest.TestCase):
    """Tests for `services/users.py - create_user()`."""

    def test_user_create_success(self):
        """With correct values, is a valid user returned?"""

        # Create demo
        demo = create_demo()
        demo_guid = loads(demo).get('guid')

        # Create new user
        user = user_service.create_user(demo_guid, 'R1')
        user_json = loads(user)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        self.assertTrue(user_json.get('id'))
        self.assertTrue(user_json.get('demoId'))
        self.assertTrue(user_json.get('email'))
        self.assertTrue(user_json.get('username'))

        # Destroy demo
        delete_demo(demo_guid)

    def test_user_create_invalid_inputs(self):
        """With an invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_guid = loads(demo).get('guid')

        # Attempt to create user with invalid inputs
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.create_user,
                          '123', 'R1')
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.create_user,
                          demo_guid, 'R99999')

        # Destroy demo
        delete_demo(demo_guid)

if __name__ == '__main__':
    unittest.main()
