def test_invalid_request(client):
    rv = client.post('/api/v1/format', json=['garbage'])

    assert rv.status_code == 400


def test_format(client):
    rv = client.post('/api/v1/format', json={
        'diff': {'N': 'b', 'O': 'a'},
        'ofmt': 'text',
    })

    assert rv.status_code == 200
    assert rv.content_type.startswith('text/plain')
    assert rv.data == b"- 'a'\n+ 'b'\n"
