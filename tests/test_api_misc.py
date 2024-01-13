def test_index(client):
    rv = client.get('/')

    assert rv.content_type.startswith('text/html')
    assert rv.status_code == 200
    assert 'ETag' in rv.headers


def test_css(client):
    rv = client.get('/api/v1/nested_diff.css')

    assert rv.content_type.startswith('text/css')
    assert rv.status_code == 200
    assert 'ETag' in rv.headers


def test_js(client):
    rv = client.get('/api/v1/nested_diff.js')

    assert rv.content_type.startswith('text/javascript')
    assert rv.status_code == 200
    assert 'ETag' in rv.headers


def test_health_check(client):
    rv = client.get('/ping')

    assert rv.content_type.startswith('text/html')
    assert rv.status_code == 200


def test_error(client):
    assert client.get('/not/exist').status_code == 404
