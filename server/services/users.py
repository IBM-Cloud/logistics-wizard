"""
Handle all actions on the user resource and is responsible for making sure
the data gets into the database. As much as possible, the interface layer should
have no knowledge of the properties of the user object and should just call
into the service layer to act upon a user resource.
"""
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from server.data.users import User, Role
from server.exceptions import (TokenException,
                               IntegrityException,
                               ResourceDoesNotExistException,
                               AuthenticationException,
                               AuthorizationException)
from server.utils import tokenize, detokenize


###########################
#         Utilities       #
###########################


def user_to_dict(user):
    """
    Convert an instance of the User model to a dict.

    :param user:  An instance of the User model.
    :return:      A dict representing the user.
    """

    return {
        'psk': user.psk,
        'user_id': user.user_id,
        'email': user.email,
        'role': user.role,
        'createdAt': user.created.isoformat()
    }


###########################
#         Services        #
###########################


def create_user(user_id=None, email=None, role=None, password=None):
    """
    Create a new user in the database.

    :param user_id:  The user's id. Optional, defaults to email.
    :param email:    The user's email address.
    :param password: The user's cleartext password (will be hashed).
    :param role:     The user's role.
    :return:         The created User model.
    """
    if user_id is None:
        user_id = email
    try:
        user = User(user_id=user_id, email=email, password=password)
        add_role_by_name(user, role)
        user.save()
    except IntegrityError as e:
        raise IntegrityException('User already exists', internal_details=str(e))
    return user


def has_permission(user, *permissions):
    """
    Verifies that a user has ALL of the permissions indicated.

    :param user:         The user to check.
    :param permissions:  A tuple of permissions to verify.
    :return:             True if all of the permissions in the list are owned
                         by the user, False otherwise.
    """
    if user is not None:
        allowed = set(permissions).issubset(set(user.permissions))
    else:
        allowed = False
    return allowed


def check_permission(user, *permissions):
    """
    Checks it the user has the specified permissions and raises an exception
    if not.

    :param user:          The user to check.
    :param permissions:   A tuple of permissions to verify.
    """
    if not has_permission(user, *permissions):
        raise AuthorizationException('Not authorized.')


def list_users():
    """
    List all users in the database

    :return:   An array of instances of Users.
    """
    return User.query.all()


def get_user_by_psk(psk):
    """
    Retrieve a user from the database by psk.

    :param psk:   The user's psk.
    :return:      An instance of the User.
    """
    user = User.query.filter(User.psk == psk).first()
    if user is None:
        raise ResourceDoesNotExistException()
    return user


def get_user_by_id(user_id):
    """
    Retrieve a user from the database by user_id.

    :param user_id:  The user's id.
    :return:         An instance of the User.
    """
    user = User.query.filter(User.user_id == user_id).first()
    if user is None:
        raise ResourceDoesNotExistException()
    return user


def get_user_by_email(email):
    """
    Retrieve a user from the database by email.

    :param email:  The user's email.
    :return:       An instance of the User.
    """
    user = User.query.filter(User.email == email).first()
    if user is None:
        raise ResourceDoesNotExistException()
    return user


def get_user_teacher_psk(user):
    """
    Get the teacher id associated with the passed in user.

    :param user:   The user for which to retrieve the teacher.
    :return:       The teacher's psk.
    """
    if user.teacher:
        teacher_psk = user.teacher.psk
    else:
        teacher_psk = None
    return teacher_psk


def get_user_school_psk(user):
    """
    Get the school id associated with the passed in user.

    :param user:   The user for which to retrieve the school.
    :return:       The school's psk.
    """
    if user.school:
        school_psk = user.school.psk
    else:
        school_psk = None
    return school_psk


def get_user_role(user):
    """
    Get the role for this user.

    :param user:    The user for which to get the role.
    :return:        The role for this user
    """
    return user.roles[0].name


def is_owner(current_user, user_resource):
    """
    Check if the one user resource owns the other user resource. This
    is a little silly for users, but makes sense for all other resources
    so we follow the same pattern to keep it all consistent.

    :param current_user:     Resource representing current user.
    :param user_resource:    Resource representing user to check.
    :return:                 True if current_user owns user_resource.
    """
    return current_user is not None and current_user.psk == user_resource.psk


def authenticate(user_id=None, password=None):
    """
    Authenticate a user against the database.

    :param user_id:
    :param password:
    :return:
    """
    try:
        user = get_user_by_id(user_id)
        if not user.verify_password(password):
            raise AuthenticationException('Invalid credentials')
    except ResourceDoesNotExistException:
        raise AuthenticationException('User does not exist')

    return user


def get_token_for_user(user, expire_days=None):
    """
    Generates an auth token for the given user.

    :param user:          The user data to be used for the token.
    :param expire_days:   The number of days until the token expires.
    :return:              A JSON Web Token.
    """
    exp = datetime.utcnow() + timedelta(days=expire_days)
    return tokenize({'psk': user.psk, 'exp': exp})


def get_user_from_token(token):
    """
    Retrieve the User model associated with this token. May raise a
    TokenException if there are any issues parsing the token.

    :param token:  A JWT token that includes the user id.
    :return:       A user object.
    """
    data = detokenize(token)
    return get_user_by_psk(data['psk'])


def generate_reset_token(psk=None, user_id=None, expire_days=1):
    """
    Generates a JSON Web Token that can be used to reset the user's
    password. By default it expires in one day.

    :param psk:          The psk of the user.
    :param user_id:      The user_id of the user.
    :param expire_days:  Days until the token expires, defaults to 1.
    :return:             A JSON Web Token.
    """
    if psk is not None:
        user = get_user_by_psk(psk)
    elif user_id is not None:
        user = get_user_by_id(user_id)
    else:
        raise ResourceDoesNotExistException()

    exp = datetime.utcnow() + timedelta(days=expire_days)
    return tokenize({'psk': user.psk,
                     'user_id': user.user_id,
                     'reset': True,
                     'exp': exp})


def reset_user_password(token=None, password=None):
    """
    Verifies that the token hasn't expired or been tampered with.
    The token should contain the user_id for which to set the password.
    If the token is empty, has expired, has been tampered with, or
    is some other type of token this will raise a TokenException.

    May raise ValidationException if password doesn't meet requirements.

    :param token:      A JSON Web Token containing the user_id
    :param password:   The new password.
    :return:
    """
    data = detokenize(token)
    # This must be a reset token, not some other token
    if 'reset' not in data:
        raise TokenException('Invalid token')

    user = get_user_by_psk(data['psk'])
    user.password = password
    user.save()


def add_role_by_name(user, *role_names):
    """
    Adds the role for the given user and commits it to the database.

    :param user:        A user object.
    :param role_names:  An array of roles to add.
    """
    for role_name in role_names:
        user.roles.append(get_role_by_name(role_name))


def get_role_by_name(role_name):
    """
    Retrieve a role from the database by name.

    :param role_name:  The name of the Role to retrieve.
    :return:           A Role object.
    """
    role = Role.query.filter(Role.name == role_name).first()
    if role is None:
        raise ResourceDoesNotExistException(
            'Role {0} does not exist.'.format(role))
    return role
