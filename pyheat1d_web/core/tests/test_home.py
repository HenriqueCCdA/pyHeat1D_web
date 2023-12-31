from http import HTTPStatus


def test_home(client):
    resp = client.get("/")

    assert resp.status_code == HTTPStatus.OK
