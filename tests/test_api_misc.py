def test_index(client):
    rv = client.get('/')

    assert rv.content_type.startswith('text/html')
    assert rv.status_code == 200


def test_health_check(client):
    rv = client.get('/ping')

    assert rv.content_type.startswith('text/html')
    assert rv.status_code == 200


def test_error(client):
    assert client.get('/not/exist').status_code == 404
