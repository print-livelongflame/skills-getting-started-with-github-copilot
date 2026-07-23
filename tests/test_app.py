import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    backup = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(backup))


def test_signup_and_unregister_participant():
    client = TestClient(app)

    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )
    assert signup_response.status_code == 200
    assert "student@mergington.edu" in activities["Chess Club"]["participants"]

    remove_response = client.delete(
        "/activities/Chess Club/participants/student@mergington.edu"
    )
    assert remove_response.status_code == 200
    assert "student@mergington.edu" not in activities["Chess Club"]["participants"]
