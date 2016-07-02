import unittest
from types import StringType
from datetime import datetime
from json import loads
from smtplib import SMTPRecipientsRefused
import server.services.messaging as messaging_service
from server.exceptions import (ValidationException,
                               UnprocessableEntityException,
                               ResourceDoesNotExistException)

###########################
#        Utilities        #
###########################


def test_user():
    """Returns a sample user object"""

    return {
        "username": "Supply Chain Manager (123)",
        "email": "chris.123@acme.com",
        "id": "123321",
        "demoId": "123321"
    }


###########################
#        Unit Tests       #
###########################

class SendEmailTestCase(unittest.TestCase):
    """Tests for `services/messaging.py"""

    def test_generate_welcome_message_success(self):
        """Is a valid welcome message string generated?"""

        # Create demo
        user = test_user()
        self.assertIsInstance(messaging_service.compose_welcome_msg("123321", user), StringType)

    def test_send_email_success(self):
        """Does the send_email function return successfully?"""

        # Create demo
        test_email = "test@example.com"
        subject = "Test Subject"
        message = messaging_service.compose_welcome_msg("123321", test_user())

        self.assertIsNone(messaging_service.send_email(test_email, subject, message, 'html'))

    def test_send_email_invalid_email(self):
        """With invalid email, is the correct exception?"""

        # Create demo
        test_email = "bad_email#example.com"
        subject = "Test Subject"
        message = messaging_service.compose_welcome_msg("123321", test_user())

        self.assertRaises(SMTPRecipientsRefused,
                          messaging_service.send_email,
                          test_email, subject, message, 'html')

if __name__ == '__main__':
    unittest.main()
