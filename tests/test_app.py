from fastapi.testclient import TestClient

from src.app import app


def test_root_redirects_to_static_index():
    client = TestClient(app)
    resp = client.get("/", follow_redirects=False)

    assert resp.status_code in (301, 302, 303, 307, 308)
    assert resp.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map():
    client = TestClient(app)
    resp = client.get("/activities")

    assert resp.status_code == 200
    data = resp.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_success_adds_participant():
    client = TestClient(app)

    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity_name}"

    # Verify it shows up in the in-memory DB via API
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_not_found():
    client = TestClient(app)

    resp = client.post("/activities/DoesNotExist/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_signup_for_activity_duplicate_is_400():
    client = TestClient(app)

    activity_name = "Chess Club"
    # One of the seeded participants in src/app.py
    email = "michael@mergington.edu"

    resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success_removes_participant():
    client = TestClient(app)

    activity_name = "Chess Club"
    email = "tempremove@mergington.edu"

    # Ensure participant exists
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    resp = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_not_found_is_404():
    client = TestClient(app)

    resp = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notinlist@mergington.edu"},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in this activity"


def test_unregister_activity_not_found_is_404():
    client = TestClient(app)

    resp = client.delete(
        "/activities/DoesNotExist/unregister",
        params={"email": "someone@mergington.edu"},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
