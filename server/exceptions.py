"""
 Global exception registry
"""


class APIException(Exception):
    """
    Generic Exception wrapper
    """

    status_code = 500

    def __init__(self, message, user_details=None, internal_details=None):
        """
        Create a new APIException

        :param message:             General exception message
        :param user_details:        Message to be shown to user
        :param internal_details:    Additional details provided by the system
        """
        self.message = message
        self.internal_details = internal_details
        if user_details is not None:
            self.user_details = user_details
        else:
            self.user_details = self.message

        super(APIException, self).__init__(self, message)

    def __str__(self):
        exception_str = super(APIException, self).__str__()
        dict_str = str(self.__dict__)
        return '{0} {1}'.format(exception_str, dict_str)

    def __unicode__(self):
        exception_str = super(APIException, self).__unicode__()
        dict_str = unicode(self.__dict__)
        return u'{0} {1}'.format(exception_str, dict_str)

    def to_dict(self):
        """
        Convert this exception to a dict for serialization.
        """
        return {
            'error': self.user_details
        }


class TokenException(APIException):
    """
    Raised when a token fails to be decoded because it is either tampered
    with or expired.
    """

    status_code = 400

    def __init__(self, message, user_details=None, internal_details=None):
        super(TokenException, self).__init__(
            message, user_details=user_details, internal_details=internal_details)


class ValidationException(APIException):
    """
    Indicates an exception when validating input data.
    """

    status_code = 400

    def __init__(self, message, user_details=None, internal_details=None):
        super(ValidationException, self).__init__(
            message, user_details=user_details, internal_details=internal_details)


class UnprocessableEntityException(APIException):
    """
    Indicates an exception when valid input is semantically incorrect.
    """

    status_code = 422

    def __init__(self, message, user_details=None, internal_details=None):
        super(UnprocessableEntityException, self).__init__(
            message, user_details=user_details, internal_details=internal_details)


class IntegrityException(APIException):
    """
    Raised when database constraints are not met on updates.
    """

    status_code = 409

    def __init__(self, message, user_details=None, internal_details=None):
        super(IntegrityException, self).__init__(
            message, user_details=user_details,
            internal_details=internal_details)


class ResourceDoesNotExistException(APIException):
    """
    Raised when retrieving a resource and it cannot be found in the database.
    """

    status_code = 404

    def __init__(self, user_details=None, internal_details=None, *args):
        if len(args) > 0:
            message = args[0]
        else:
            message = 'Resource does not exist.'
        super(ResourceDoesNotExistException, self).__init__(
            message, user_details=user_details,
            internal_details=internal_details)


class AuthenticationException(APIException):
    """
    Raised when authentication fails for any reason.
    """

    status_code = 401

    def __init__(self, message, user_details=None, internal_details=None):
        super(AuthenticationException, self).__init__(
            message, user_details=user_details,
            internal_details=internal_details)


class AuthorizationException(APIException):
    """
    Raised when a user tries to access something without proper permissions.
    """

    status_code = 401

    def __init__(self, message, user_details=None, internal_details=None):
        super(AuthorizationException, self).__init__(
            message, user_details=user_details,
            internal_details=internal_details)
