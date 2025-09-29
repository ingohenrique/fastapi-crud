API_PREFIX = "/api/v1"

def test_create_user(client):
    response = client.post(f"{API_PREFIX}/users/", json={
        "name": "test",
        "email": "email@public.com"
    })
    assert response.status_code == 201

def test_create_user_invalid_email(client):
    response = client.post(f"{API_PREFIX}/users/", json={
        "name": "test",
        "email": "invalid-email"
    })
    assert response.status_code == 422

def test_create_user_with_existing_email(client):
    response = client.post(f"{API_PREFIX}/users/", json={
        "name": "test",
        "email": "email@public.com"
    })
    assert response.status_code == 400
