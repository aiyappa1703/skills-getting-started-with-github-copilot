"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient for making requests to the FastAPI app.
    Resets in-memory activities before each test to ensure test isolation.
    """
    # Reset activities to initial state before each test
    activities.clear()
    activities.update({
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
        "Basketball Team": {
            "description": "Competitive basketball training and matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Soccer practice and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["ryan@mergington.edu", "jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and digital art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu"]
        },
        "Drama Club": {
            "description": "Stage acting and theatrical performances",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["james@mergington.edu", "sophie@mergington.edu"]
        },
        "Math Club": {
            "description": "Problem solving and preparation for math competitions",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        }
    })
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """
    Provide sample activity data for testing.
    """
    return {
        "name": "Test Activity",
        "description": "A test activity for unit testing",
        "schedule": "Monday, 3:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": ["test1@mergington.edu", "test2@mergington.edu"]
    }


@pytest.fixture
def sample_emails():
    """
    Provide sample email addresses for testing signup/unregister functionality.
    """
    return {
        "existing": "michael@mergington.edu",  # Already signed up for Chess Club
        "new": "newstudent@mergington.edu",    # Not yet signed up
        "another_new": "anotherstudent@mergington.edu"
    }
