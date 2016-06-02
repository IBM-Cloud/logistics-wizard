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
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_guid = loads(demo).get('guid')

        # Attempt to create user with invalid inputs
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.create_user,
                          'ABC123', 'R1')
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.create_user,
                          demo_guid, 'R99999')

        # Destroy demo
        delete_demo(demo_guid)


class UserLoginTestCase(unittest.TestCase):
    """Tests for `services/users.py - login()`."""

    def test_user_login_success(self):
        """With correct values, is a valid user logged in?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        self.assertTrue(auth_data.get('loopback_token'))
        self.assertTrue(auth_data.get('user'))

        user_json = auth_data.get('user')
        self.assertTrue(user_json.get('id'))
        self.assertTrue(user_json.get('demoId'))
        self.assertTrue(user_json.get('username'))
        self.assertTrue(user_json.get('email'))

        if user_json.get('roles'):
            for role_json in user_json.get('roles'):
                self.assertTrue(role_json.get('id'))
                self.assertTrue(role_json.get('name'))
                self.assertTrue(role_json.get('created'))
                self.assertTrue(role_json.get('modified'))

        # Destroy demo
        delete_demo(demo_guid)

    def test_user_login_invalid_inputs(self):
        """With invalid inputs, are correct errors thrown?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Attempt to create user with invalid inputs
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.login,
                          'ABC123', demo_user_id)
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.login,
                          demo_guid, '9283742b918a9367c83b4c4d4e327ed7')

        # Destroy demo
        delete_demo(demo_guid)


class UserLogoutTestCase(unittest.TestCase):
    """Tests for `services/users.py - logout()`."""

    def test_user_logout_success(self):
        """With correct values, is a valid user logged out?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user
        auth_data = user_service.login(demo_guid, demo_user_id)
        loopback_token = auth_data.get('loopback_token')

        # Log out user
        self.assertTrue(user_service.logout(loopback_token) is None)

        # Destroy demo
        delete_demo(demo_guid)

    def test_user_logout_invalid_token(self):
        """With an invalid token, are correct errors thrown?"""

        # Log out with bad token
        bad_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJu" \
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

        # Attempt to log out user with invalid token
        self.assertRaises(ResourceDoesNotExistException,
                          user_service.logout,
                          bad_token)


class TokenizeTestCase(unittest.TestCase):
    """Tests for `services/users.py - get_token_for_user() and get_auth_from_token()`."""

    def test_tokenize_and_detokenize(self):
        """Is auth data correctly tokenized and later detokenized?"""

        # Create demo
        demo = create_demo()
        demo_json = loads(demo)
        demo_guid = demo_json.get('guid')
        demo_user_id = demo_json.get('users')[0].get('id')

        # Log in user and tokenize auth data
        auth_data = user_service.login(demo_guid, demo_user_id)
        token = user_service.get_token_for_user(auth_data, expire_days=14)

        # Detokenize auth data
        decrypted_auth_data = user_service.get_auth_from_token(token)

        # Check that decrypted data is equivalent to auth data
        self.assertTrue(auth_data.get('loopback_token') ==
                        decrypted_auth_data.get('loopback_token'))
        self.assertTrue(auth_data.get('exp') ==
                        decrypted_auth_data.get('exp'))
        self.assertTrue(auth_data.get('user').get('id') ==
                        decrypted_auth_data.get('user').get('id'))

        # Destroy demo
        delete_demo(demo_guid)

if __name__ == '__main__':
    unittest.main()
