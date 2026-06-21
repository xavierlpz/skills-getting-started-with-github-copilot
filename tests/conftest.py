"""
Pytest configuration and shared fixtures for FastAPI tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def test_client():
    """Provides a FastAPI TestClient for making requests to the app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test to ensure test isolation"""
    # Reset participants to initial state
    from src.app import activities
    
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Competitive soccer practice and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["nina@mergington.edu", "kevin@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and water safety activities",
            "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["lisa@mergington.edu", "aaron@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["maya@mergington.edu", "jazmine@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stage production, and theater workshops",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["ryan@mergington.edu", "sophia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking, argumentation, and debate competition",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["alex@mergington.edu", "zoe@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Prepare for math competitions and sharpen problem-solving skills",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 10,
            "participants": ["ethan@mergington.edu", "mia@mergington.edu"]
        }
    }
    
    # Clear and reset activities dictionary
    activities.clear()
    activities.update(initial_activities)
    
    yield
