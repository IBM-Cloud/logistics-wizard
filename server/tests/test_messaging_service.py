import unittest
from types import StringType
from smtplib import SMTPRecipientsRefused
import server.services.messaging as messaging_service


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(SendEmailTestCase('test_generate_welcome_message_success'))
    test_suite.addTest(SendEmailTestCase('test_send_email_success'))
    test_suite.addTest(SendEmailTestCase('test_send_email_invalid_email'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class SendEmailTestCase(unittest.TestCase):
    """Tests for `services/messaging.py"""

    def setUp(self):
        # Create dummy message
        self.subject = "Test Subject"
        test_user = {
            "username": "Supply Chain Manager (123)",
            "email": "chris.123@acme.com",
            "id": 123321,
            "demoId": 123321
        }
        self.message = messaging_service.compose_msg('welcome.html', ("123321",
                                                                      test_user.get('username'),
                                                                      str(test_user.get('id'))))

    def test_generate_welcome_message_success(self):
        """Is a valid welcome message string generated?"""

        self.assertIsInstance(self.message, StringType)

    def test_send_email_success(self):
        """Does the send_email function return successfully?"""

        self.assertIsNone(messaging_service.send_email("test@example.com", self.subject, self.message, 'html'))

    def test_send_email_invalid_email(self):
        """With invalid email, is the correct exception?"""

        self.assertRaises(SMTPRecipientsRefused,
                          messaging_service.send_email,
                          "bad_email#example.com", self.subject, self.message, 'html')

if __name__ == '__main__':
    unittest.main()
