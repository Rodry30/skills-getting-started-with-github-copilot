def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"]


def test_signup_for_activity_adds_student(client):
    response = client.post("/activities/Chess%20Club/signup?email=student@example.com")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@example.com for Chess Club"

    activities_response = client.get("/activities")
    assert "student@example.com" in activities_response.json()["Chess Club"]["participants"]


def test_signup_for_activity_rejects_duplicate_email(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_activity_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_rejects_empty_email(client):
    response = client.post("/activities/Chess%20Club/signup?email=   ")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"


def test_remove_participant_from_activity(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_remove_participant_rejects_unknown_student(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=missing@example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"