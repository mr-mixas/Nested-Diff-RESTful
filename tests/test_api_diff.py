def test_invalid_request(client):
    rv = client.post('/api/v1/diff', json=['garbage'])

    assert rv.status_code == 400


def test_default(client):
    rv = client.post('/api/v1/diff', json={'a': 'a', 'b': 'b'})

    assert rv.status_code == 200
    assert rv.content_type == 'application/json'
    assert rv.get_json() == {'N': 'b', 'O': 'a'}


def test_diff_opts(client):
    rv = client.post('/api/v1/diff', json={
        'a': 'a',
        'b': 'b',
        'diff_opts': {'O': False},
    })

    assert rv.status_code == 200
    assert rv.content_type == 'application/json'
    assert rv.get_json() == {'N': 'b'}


def test_ofmt_text(client):
    rv = client.post('/api/v1/diff', json={
        'a': 'a',
        'b': 'b',
        'diff_opts': {'O': False},
        'ofmt': 'text',
    })

    assert rv.status_code == 200
    assert rv.content_type.startswith('text/plain')
    assert rv.data == b"+ 'b'\n"


def test_ofmt_term(client):
    rv = client.post('/api/v1/diff', json={
        'a': 'a',
        'b': 'b',
        'diff_opts': {'O': False},
        'ofmt': 'term',
    })

    assert rv.status_code == 200
    assert rv.content_type.startswith('text/plain')
    assert rv.data == b"\x1b[32m+ 'b'\x1b[0m\n"
