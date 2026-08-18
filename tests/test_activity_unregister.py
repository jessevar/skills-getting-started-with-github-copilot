from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
        }
    )


def test_unregister_participant_removes_email_from_activity():
    reset_activities()

    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name)

    response = client.delete(f"/activities/{encoded_activity}/participants/{quote(email)}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert "Unregistered" in response.json()["message"]
