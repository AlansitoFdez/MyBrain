def test_register(client):
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test1234"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "testuser"
    assert "hashed_password" not in data

def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test1234"
    })
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser2",
        "password": "test1234"
    })
    assert response.status_code == 400

def test_login(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test1234"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "test1234"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test1234"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401