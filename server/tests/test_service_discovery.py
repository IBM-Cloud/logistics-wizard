import unittest
from json import loads
import server.tests.utils as utils
import server.services.service_discovery as service_discovery_service
from server.exceptions import (ValidationException,
                               ResourceDoesNotExistException)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(RegisterServiceTestCase('test_register_service_success'))
    test_suite.addTest(RegisterServiceTestCase('test_register_service_invalid_input'))
    test_suite.addTest(HeartbeatServiceTestCase('test_heartbeat_service_success'))
    test_suite.addTest(HeartbeatServiceTestCase('test_heartbeat_service_invalid_input'))
    test_suite.addTest(DeregisterServiceTestCase('test_deregister_service_success'))
    test_suite.addTest(DeregisterServiceTestCase('test_deregister_service_invalid_input'))
    test_suite.addTest(GetServicesTestCase('test_get_services_success'))
    test_suite.addTest(GetServicesTestCase('test_get_services_filter_success'))
    test_suite.addTest(GetServicesTestCase('test_get_services_invalid_filter'))
    return test_suite


###########################
#        Unit Tests       #
###########################

class RegisterServiceTestCase(unittest.TestCase):
    """Tests for `services/service_discovery.py - register_service()`."""

    def setUp(self):
        self.service_name = 'lw-test'
        self.endpoint = 'https://logistics-wizard-test.mybluemix.net'

    def test_register_service_success(self):
        """With correct values, is the service registered?"""

        # Register service
        service = service_discovery_service.register_service(self.service_name, 300, 'UP',
                                                             self.endpoint, 'http', heartbeat=False)

        # TODO: Update to use assertIsInstance(a,b)
        # Check that the service was successfully registered
        service_json = loads(service)
        self.assertTrue(service_json.get('id'))
        self.assertEqual(service_json.get('ttl'), 300)
        if service_json.get('links'):
            self.assertTrue(service_json.get('links').get('self'))
            self.assertTrue(service_json.get('links').get('heartbeat'))

        # De-register service
        service_discovery_service.deregister_service(service_json.get('id'))

    def test_register_service_invalid_input(self):
        """With invalid inputs, is correct error thrown?"""

        # Attempt to register a service with invalid status and protocol
        self.assertRaises(ValidationException,
                          service_discovery_service.register_service,
                          self.service_name, 300, 'UPPER', self.endpoint, 'http', heartbeat=False)
        self.assertRaises(ValidationException,
                          service_discovery_service.register_service,
                          self.service_name, 300, 'UP', self.endpoint, 'odb', heartbeat=False)


class HeartbeatServiceTestCase(unittest.TestCase):
    """Tests for `services/service_discovery.py - heartbeat_service()`."""

    def setUp(self):
        self.service_id = loads(service_discovery_service.
                                register_service('lw-test', 300, 'UP',
                                                 'https://logistics-wizard-test.mybluemix.net',
                                                 'http', heartbeat=False)).get('id')

    def test_heartbeat_service_success(self):
        """With correct values, is the service heartbeated?"""
        self.assertTrue(service_discovery_service.heartbeat_service(self.service_id) is None)

    def test_heartbeat_service_invalid_input(self):
        """With invalid inputs, is correct error thrown?"""

        # Attempt to heartbeat a nonexistent service instance
        self.assertRaises(ResourceDoesNotExistException,
                          service_discovery_service.heartbeat_service,
                          'ABC123')

    def tearDown(self):
        # De-register service
        service_discovery_service.deregister_service(self.service_id)


class DeregisterServiceTestCase(unittest.TestCase):
    """Tests for `services/service_discovery.py - deregister_service()`."""

    def setUp(self):
        self.service_id = loads(service_discovery_service.
                                register_service('lw-test', 300, 'UP',
                                                 'https://logistics-wizard-test.mybluemix.net',
                                                 'http', heartbeat=False)).get('id')

    def test_deregister_service_success(self):
        """With correct values, is the service deregistered?"""
        self.assertTrue(service_discovery_service.deregister_service(self.service_id) is None)

    def test_deregister_service_invalid_input(self):
        """With invalid inputs, is correct error thrown?"""

        # Attempt to deregister a nonexistent service instance
        self.assertRaises(ResourceDoesNotExistException,
                          service_discovery_service.deregister_service,
                          'ABC123')


class GetServicesTestCase(unittest.TestCase):
    """Tests for `services/service_discovery.py - get_services()`."""

    def setUp(self):
        self.service_id_1 = loads(service_discovery_service.
                                  register_service('lw-test1', 300, 'UP',
                                                   'https://logistics-wizard-test1.mybluemix.net',
                                                   'http', heartbeat=False,
                                                   tags=['lw-test'])).get('id')
        self.service_id_2 = loads(service_discovery_service.
                                  register_service('lw-test2', 300, 'UP',
                                                   'https://logistics-wizard-test2.mybluemix.net',
                                                   'http', heartbeat=False,
                                                   tags=['lw-test', 'db'])).get('id')

    def test_get_services_success(self):
        """With correct values, is the service deregistered?"""
        services = loads(service_discovery_service.get_services()).get('instances')

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
        services = loads(service_discovery_service.get_services(fields='id,service_name')).get('instances')
        for instance in services:
            self.assertTrue(instance.get('id'))
            self.assertTrue(instance.get('service_name'))
            self.assertTrue(instance.get('status') is None)

        # Test the 'tags' filter
        services = loads(service_discovery_service.get_services(tags='lw-test')).get('instances')
        service_ids = [self.service_id_1, self.service_id_2]
        for instance in services:
            self.assertIn(instance.get('id'), service_ids)

        # Test the 'service_name' filter
        services = loads(service_discovery_service.get_services(service_name='lw-test1')).get('instances')
        for instance in services:
            self.assertEqual(instance.get('id'), self.service_id_1)

        # Test the 'status' filter
        services = loads(service_discovery_service.get_services(status='UP')).get('instances')
        for instance in services:
            self.assertEqual(instance.get('status'), 'UP')

    def test_get_services_invalid_filter(self):
        """With invalid filters, is correct error thrown?"""

        # Attempt to retrieve services with invalid 'fields' filter
        self.assertRaises(ValidationException,
                          service_discovery_service.get_services,
                          fields='dummy')

    def tearDown(self):
        # De-register service
        service_discovery_service.deregister_service(self.service_id_1)
        service_discovery_service.deregister_service(self.service_id_2)

if __name__ == '__main__':
    unittest.main()
