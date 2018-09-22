import os
import tempfile

import pytest

from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_unhauthorized(client):
    """request response should be unhauthorized"""

    rv = client.get('/tweets')
    assert b'Invalid token' in rv.data