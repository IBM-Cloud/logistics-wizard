"""
Contains database scripts to initialize/modify the database
on app startup.
"""
from datetime import datetime, timedelta

from server.data.tools import db_script
from server.data.users import User, Role, Permission


@db_script(envs='ALL')
def add_initial_roles():
    """
    Setup the initial roles/permissions
    """
    admin = Role(name='admin')
    supply_chain_manager = Role(name='supplychainmanager')
    retail_store_manager = Role(name='retailstoremanager')

    # Initial permissions
    view_users = Permission(name='view_users')
    edit_users = Permission(name='edit_users')

    # Admin permissions
    admin.permissions.append(view_users)
    admin.permissions.append(edit_users)

    admin.save()
    supply_chain_manager.save()
    retail_store_manager.save()


@db_script(envs=['DEV', 'TEST'])
def add_admin_user():
    admin = User(user_id='admin@admin.com',
                 email='admin@admin.com',
                 password='password')
    role = Role.query.filter(Role.name == 'admin').first()
    admin.roles.append(role)
    admin.save()


@db_script(envs=['DEV'])
def create_dev_supply_chain_manager():
    user = User(user_id='chris@company.com',
                email='chris@company.com',
                password='password')

    user.roles.append(Role.query.filter(Role.name == 'supplychainmanager').first())
    user.save()


@db_script(envs=['DEV'])
def create_dev_retail_store_manager():
    user = User(user_id='ruth@company.com',
                email='ruth@company.com',
                password='password')

    user.roles.append(Role.query.filter(Role.name == 'retailstoremanager').first())
    user.save()


@db_script(envs='ALL')
def create_shipment_permissions():
    supply_chain_manager = Role.query.filter(Role.name == 'supplychainmanager').first()
    retailstoremanager = Role.query.filter(Role.name == 'retailstoremanager').first()

    create_shipments = Permission(name='create_shipment')
    view_shipments = Permission(name='view_shipment')
    edit_shipments = Permission(name='edit_shipment')
    delete_shipments = Permission(name='delete_shipment')

    supply_chain_manager.permissions.append(create_shipments)
    supply_chain_manager.permissions.append(view_shipments)
    supply_chain_manager.permissions.append(edit_shipments)
    supply_chain_manager.permissions.append(delete_shipments)

    retailstoremanager.permissions.append(create_shipments)
    retailstoremanager.permissions.append(view_shipments)
    retailstoremanager.permissions.append(edit_shipments)
    retailstoremanager.permissions.append(delete_shipments)

    supply_chain_manager.save()
    retailstoremanager.save()


@db_script(envs='ALL')
def create_distribution_center_permissions():
    supply_chain_manager = Role.query.filter(Role.name == 'supplychainmanager').first()
    retailstoremanager = Role.query.filter(Role.name == 'retailstoremanager').first()

    view_distribution_centers = Permission(name='view_distribution_center')

    supply_chain_manager.permissions.append(view_distribution_centers)
    retailstoremanager.permissions.append(view_distribution_centers)

    supply_chain_manager.save()
    retailstoremanager.save()


@db_script(envs='ALL')
def create_retailer_permissions():
    supply_chain_manager = Role.query.filter(Role.name == 'supplychainmanager').first()
    retailstoremanager = Role.query.filter(Role.name == 'retailstoremanager').first()

    view_retailers = Permission(name='view_retailer')

    supply_chain_manager.permissions.append(view_retailers)
    retailstoremanager.permissions.append(view_retailers)

    supply_chain_manager.save()
    retailstoremanager.save()


@db_script(envs='ALL')
def create_recommendation_permissions():
    supply_chain_manager = Role.query.filter(Role.name == 'supplychainmanager').first()
    retailstoremanager = Role.query.filter(Role.name == 'retailstoremanager').first()

    view_recommendations = Permission(name='view_recommendation')
    edit_recommendations = Permission(name='edit_recommendation')

    supply_chain_manager.permissions.append(view_recommendations)
    supply_chain_manager.permissions.append(edit_recommendations)

    retailstoremanager.permissions.append(view_recommendations)
    retailstoremanager.permissions.append(edit_recommendations)

    supply_chain_manager.save()
    retailstoremanager.save()


@db_script(envs='ALL')
def create_session_permissions():
    admin = Role.query.filter(Role.name == 'admin').first()

    delete_sessions = Permission(name='delete_sessions')

    admin.permissions.append(delete_sessions)

    admin.save()
