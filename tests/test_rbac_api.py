import pytest

def get_token(client, username, password):
    response = client.post("/auth/login", data={"username": username, "password": password, "grant_type": "password"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_admin_access_admin(client):
    token = get_token(client, "admin", "admin123")
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_viewer_blocked_from_admin(client):
    token = get_token(client, "viewer", "viewer123")
    response = client.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_viewer_access_public(client):
    token = get_token(client, "viewer", "viewer123")
    response = client.get("/viewer/public-data", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_invalid_token_rejected(client):
    response = client.get("/admin/users", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
