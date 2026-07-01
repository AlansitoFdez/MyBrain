def get_auth_client(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "test1234"
    })
    client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "test1234"
    })
    return client

def test_create_note(client):
    auth_client = get_auth_client(client)
    response = auth_client.post("/notes/", json={
        "title": "Test note",
        "content": "Test content"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test note"
    assert data["content"] == "Test content"

def test_get_notes(client):
    auth_client = get_auth_client(client)
    auth_client.post("/notes/", json={"title": "Nota 1", "content": "Contenido 1"})
    auth_client.post("/notes/", json={"title": "Nota 2", "content": "Contenido 2"})
    response = auth_client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_note(client):
    auth_client = get_auth_client(client)
    create = auth_client.post("/notes/", json={"title": "Original", "content": "Original"})
    note_id = create.json()["id"]
    response = auth_client.put(f"/notes/{note_id}", json={"title": "Actualizado"})
    assert response.status_code == 200
    assert response.json()["title"] == "Actualizado"
    assert response.json()["content"] == "Original"

def test_delete_note(client):
    auth_client = get_auth_client(client)
    create = auth_client.post("/notes/", json={"title": "A borrar", "content": "contenido"})
    note_id = create.json()["id"]
    response = auth_client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    notes = auth_client.get("/notes")
    assert len(notes.json()) == 0

def test_cannot_access_other_user_note(client):
    auth_client = get_auth_client(client)
    create = auth_client.post("/notes/", json={"title": "Mi nota", "content": "privada"})
    note_id = create.json()["id"]

    client.post("/auth/register", json={
        "email": "other@test.com",
        "username": "otheruser",
        "password": "test1234"
    })
    client.post("/auth/login", json={
        "email": "other@test.com",
        "password": "test1234"
    })
    response = client.put(f"/notes/{note_id}", json={"title": "Hackeado"})
    assert response.status_code == 404