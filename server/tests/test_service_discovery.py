import unittest
from types import StringType
from json import loads
from os import environ as env
from server.service_discovery import ServicePublisher, ServiceLocator


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(RegisterServiceTestCase('test_register_service_success'))
    test_suite.addTest(RegisterServiceTestCase('test_register_service_invalid_input'))
    test_suite.addTest(HeartbeatServiceTestCase('test_heartbeat_service_success'))
    test_suite.addTest(HeartbeatServiceTestCase('test_heartbeating_success'))
    test_suite.addTest(HeartbeatServiceTestCase('test_heartbeat_service_unregistered_publisher'))
    test_suite.addTest(HeartbeatServiceTestCase('test_get_last_heartbeat_success'))
    test_suite.addTest(DeregisterServiceTestCase('test_deregister_service_success'))
    test_suite.addTest(GetServicesTestCase('test_get_services_success'))
    test_suite.addTest(GetServicesTestCase('test_get_services_filter_success'))
    test_suite.addTest(GetServicesTestCase('test_get_services_invalid_input'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class RegisterServiceTestCase(unittest.TestCase):
    """Tests for `ServicePublisher.register_service()."""

    def setUp(self):
        self.service_name = 'lw-test'
        self.endpoint = 'https://logistics-wizard-test.mybluemix.net'

    def test_register_service_success(self):
        """With correct values, is the service registered?"""

        # Register service
        publisher = ServicePublisher(self.service_name, 300, 'UP', self.endpoint, 'http',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        service = publisher.register_service(False)

        # TODO: Update to use assertIsInstance(a,b)
        # Check that the service was successfully registered
        self.assertTrue(publisher.registered)
        service_json = loads(service)
        self.assertTrue(service_json.get('id'))
        self.assertEqual(service_json.get('ttl'), 300)
        if service_json.get('links'):
            self.assertTrue(service_json.get('links').get('self'))
            self.assertTrue(service_json.get('links').get('heartbeat'))

        # De-register service
        publisher.deregister_service()

    def test_register_service_invalid_input(self):
        """With invalid inputs, is correct error thrown?"""

        # No auth token
        self.assertRaises(Exception, ServicePublisher,
                          self.service_name, 300, 'UPPER', self.endpoint, 'http')

        # Invalid status
        publisher = ServicePublisher(self.service_name, 300, 'UPPER', self.endpoint, 'http',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        self.assertRaises(Exception, publisher.register_service, False)
        self.assertFalse(publisher.registered)

        # Invalid protocol
        publisher = ServicePublisher(self.service_name, 300, 'UP', self.endpoint, 'odb',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        self.assertRaises(Exception, publisher.register_service, False)
        self.assertFalse(publisher.registered)

        # Invalid Service Discover auth token
        publisher = ServicePublisher(self.service_name, 300, 'UP', self.endpoint, 'odb',
                                     url=env['SD_URL'], auth_token='ABC123')
        self.assertRaises(Exception, publisher.register_service, False)
        self.assertFalse(publisher.registered)


class HeartbeatServiceTestCase(unittest.TestCase):
    """Tests for ServicePublisher.heartbeat_service()."""

    def setUp(self):
        self.service_name = 'lw-test'
        self.endpoint = 'https://logistics-wizard-test.mybluemix.net'

    def test_heartbeat_service_success(self):
        """With correct values, is the service heartbeated?"""
        publisher = ServicePublisher(self.service_name, 300, 'UP', self.endpoint, 'http',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        publisher.register_service(False)
        self.assertIsInstance(publisher.heartbeat_service(), StringType)
        publisher.deregister_service()

    def test_heartbeating_success(self):
        """With correct values, does the heartbeating process complete?"""
        import time
        publisher = ServicePublisher(self.service_name, 30, 'UP', self.endpoint, 'http',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        publisher.register_service(True)
        time.sleep(2)
        publisher.deregister_service()

    def test_heartbeat_service_unregistered_publisher(self):
        """With invalid inputs, is correct error thrown?"""

        # Attempt to heartbeat a non-registered publisher
        publisher = ServicePublisher(self.service_name, 300, 'UP', self.endpoint, 'http',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        self.assertRaises(Exception, publisher.heartbeat_service)

    def test_get_last_heartbeat_success(self):
        """With invalid inputs, is correct error thrown?"""

        # Attempt to heartbeat a non-registered publisher
        publisher = ServicePublisher(self.service_name, 300, 'UP', self.endpoint, 'http',
                                     url=env['SD_URL'], auth_token=env['SD_AUTH'])
        publisher.register_service(False)
        self.assertEqual(publisher.get_last_heartbeat(), '')
        heartbeat_time = publisher.heartbeat_service()
        self.assertEqual(publisher.get_last_heartbeat(), heartbeat_time)
        publisher.deregister_service()


class DeregisterServiceTestCase(unittest.TestCase):
    """Tests for ServicePublisher.deregister_service()."""

    def setUp(self):
        self.publisher = ServicePublisher('lw-test', 300, 'UP', 'https://logistics-wizard-test.mybluemix.net', 'http',
                                          url=env['SD_URL'], auth_token=env['SD_AUTH'])
        self.publisher.register_service(False)

    def test_deregister_service_success(self):
        """With correct values, is the service deregistered?"""
        self.assertTrue(self.publisher.deregister_service() is None)


class GetServicesTestCase(unittest.TestCase):
    """Tests for ServicePublisher.get_services()."""

    def setUp(self):
        # Register two services
        self.publisher_1 = ServicePublisher('lw-test1', 300, 'UP', 'https://logistics-wizard-test1.mybluemix.net', 'http',
                                            tags=['lw-test'], url=env['SD_URL'], auth_token=env['SD_AUTH'])
        self.publisher_1.register_service(False)
        self.publisher_2 = ServicePublisher('lw-test2', 300, 'UP', 'https://logistics-wizard-test2.mybluemix.net', 'http',
                                            tags=['lw-test', 'db'], url=env['SD_URL'], auth_token=env['SD_AUTH'])
        self.publisher_2.register_service(False)

    def test_get_services_success(self):
        """With correct values, is the service deregistered?"""
        locator = ServiceLocator(env['SD_URL'], env['SD_AUTH'])
        services = loads(locator.get_services()).get('instances')

        # TODO: Update to use assertIsInstance(a,b)
        for instance in services:
            self.assertTrue(instance.get('id'))
            self.assertTrue(instance.get('service_name'))
            self.assertTrue(instance.get('ttl'))
            self.assertTrue(instance.get('status'))
            self.assertTrue(instance.get('endpoint').get('type'))
            self.assertTrue(instance.get('endpoint').get('value'))

    def test_get_services_filter_success(self):
        """Are correct services returned?"""

        # Test the 'fields' filter
        locator = ServiceLocator(env['SD_URL'], env['SD_AUTH'])
        services = loads(locator.get_services(fields='id,service_name')).get('instances')
        for instance in services:
            self.assertTrue(instance.get('id'))
            self.assertTrue(instance.get('service_name'))
            self.assertTrue(instance.get('status') is None)

        # Test the 'tags' filter
        services = loads(locator.get_services(tags='lw-test')).get('instances')
        service_ids = [self.publisher_1.id, self.publisher_2.id]
        for instance in services:
            self.assertIn(instance.get('id'), service_ids)

        # Test the 'service_name' filter
        services = loads(locator.get_services(service_name='lw-test1')).get('instances')
        for instance in services:
            self.assertEqual(instance.get('id'), self.publisher_1.id)

        # Test the 'status' filter
        services = loads(locator.get_services(status='UP')).get('instances')
        for instance in services:
            self.assertEqual(instance.get('status'), 'UP')

    def test_get_services_invalid_input(self):
        """With invalid filters, is correct error thrown?"""

        # Attempt to retrieve services with invalid 'fields' filter
        locator = ServiceLocator(env['SD_URL'], env['SD_AUTH'])
        self.assertRaises(Exception, locator.get_services, fields='dummy')

        # Attempt to retrieve services with invalid auth
        locator = ServiceLocator(env['SD_URL'], 'ABC123')
        self.assertRaises(Exception, locator.get_services)

    def tearDown(self):
        # De-register service
        self.publisher_1.deregister_service()
        self.publisher_2.deregister_service()

if __name__ == '__main__':
    unittest.main()
