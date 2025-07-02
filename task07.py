import pytest
from fastapi.testclient import TestClient
from fastapi import status
from fastapi_auth_crud import app  # Предполагаем, что файл с приложением называется fastapi_auth_crud.py

client = TestClient(app)

# ------------------ /auth/register ------------------
def test_register_success():
    response = client.post("/auth/register", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["message"] == "User registered"

def test_register_duplicate():
    client.post("/auth/register", data={"username": "dupeuser", "password": "pass"})
    response = client.post("/auth/register", data={"username": "dupeuser", "password": "pass"})
    assert response.status_code == 400

# ------------------ /auth/token ------------------
def test_login_success():
    client.post("/auth/register", data={"username": "logintest", "password": "testpass"})
    response = client.post("/auth/token", data={"username": "logintest", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/auth/token", data={"username": "nosuchuser", "password": "wrong"})
    assert response.status_code == 400

# ------------------ /auth/me ------------------
def test_get_me_success():
    client.post("/auth/register", data={"username": "meuser", "password": "pass"})
    token = client.post("/auth/token", data={"username": "meuser", "password": "pass"}).json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"

def test_get_me_unauthorized():
    response = client.get("/auth/me")
    assert response.status_code == 401

# ------------------ /protected ------------------
def test_protected_route_authorized():
    client.post("/auth/register", data={"username": "secureuser", "password": "pass"})
    token = client.post("/auth/token", data={"username": "secureuser", "password": "pass"}).json()["access_token"]
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert f"secureuser" in response.json()["message"]

def test_protected_route_unauthorized():
    response = client.get("/protected")
    assert response.status_code == 401
