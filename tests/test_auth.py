import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Use in-memory SQLite DB for tests before importing app
os.environ['PLANNER_DATABASE_URI'] = 'sqlite:///:memory:'

import app as planner
from flask import g


def setup_client():
    """Create a test client with initialized database."""
    with planner.app.app_context():
        planner.create_tables()
    return planner.app.test_client()


def test_register_login_logout():
    client = setup_client()

    # Registration logs in the user automatically
    resp = client.post('/register', data={
        'username': 'alice',
        'password': 'secret'
    }, follow_redirects=True)
    assert 'Willkommen zum Planer' in resp.get_data(as_text=True)

    # Logout and ensure protected route redirects
    client.get('/logout')
    resp = client.get('/tickets')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']

    # Log in again
    resp = client.post('/login', data={
        'username': 'alice',
        'password': 'secret'
    }, follow_redirects=True)
    assert 'Willkommen zum Planer' in resp.get_data(as_text=True)

    # Authenticated access to protected route
    resp = client.get('/tickets')
    assert resp.status_code == 200


def test_invalid_login():
    client = setup_client()

    resp = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong'
    }, follow_redirects=True)
    assert 'Ungültige Zugangsdaten' in resp.get_data(as_text=True)


