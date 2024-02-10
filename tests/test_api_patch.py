def test_invalid_request(client):
    rv = client.post('/api/v1/patch', json=['garbage'])

    assert rv.status_code == 400


def test_patch(client):
    rv = client.post(
        '/api/v1/patch',
        json={'target': 'a', 'patch': {'N': 'b'}},
    )

    assert rv.status_code == 200
    assert rv.content_type == 'application/json'
    assert rv.get_json() == 'b'
