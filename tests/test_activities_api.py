from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()
    assert response.json()["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_registers_new_participant(client):
    response = client.post("/activities/Chess Club/signup?email=alex@mergington.edu")

    assert response.status_code == 200
    assert "alex@mergington.edu" in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Signed up alex@mergington.edu for Chess Club"


def test_signup_rejects_duplicate_participant(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/{quote('Chess Club')}/participants/{quote(email)}")

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert "Unregistered" in response.json()["message"]


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(f"/activities/{quote('Chess Club')}/participants/{quote('unknown@mergington.edu')}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
