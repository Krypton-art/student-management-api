def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Student Management API"
    }

def test_create_student(client):
    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "age": 22,
            "branch": "CSE"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Student"
    assert data["age"] == 22
    assert data["branch"] == "CSE"
    assert "id" in data

def test_get_students(client):
    client.post(
        "/students/",
        json={
            "name": "Somya",
            "age": 22,
            "branch": "CSE"
        }
    )

    response = client.get("/students/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Somya"

def test_get_student_not_found(client):
    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_create_invalid_student(client):
    response = client.post(
        "/students/",
        json={
            "name": "S",
            "age": 150,
            "branch": ""
        }
    )

    assert response.status_code == 422

def test_update_student(client):
    create_response = client.post(
        "/students/",
        json={
            "name": "Somya",
            "age": 22,
            "branch": "CSE"
        }
    )

    student_id = create_response.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "Somya Sharma",
            "age": 23,
            "branch": "CSE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["name"] == "Somya Sharma"
    assert data["age"] == 23
    assert data["branch"] == "CSE"

def test_delete_student(client):
    create_response = client.post(
        "/students/",
        json={
            "name": "Vanu",
            "age": 21,
            "branch": "CSE"
        }
    )

    student_id = create_response.json()["id"]

    response = client.delete(
        f"/students/{student_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/students/{student_id}"
    )

    assert get_response.status_code == 404