"""
Unit tests for the FastAPI backend using AAA (Arrange-Act-Assert) pattern.
Tests individual components and business logic.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import activities


class TestActivitiesDataStructure:
    """Test the activities data structure and validation logic."""
    
    def test_activities_initialized_with_data(self):
        """
        Verify that the activities dictionary is initialized with expected data.
        
        AAA Pattern:
        - Arrange: Access the activities dictionary
        - Act: Check if it contains expected activities
        - Assert: Verify all required activities are present
        """
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", 
            "Basketball Team", "Soccer Club", "Art Studio", 
            "Drama Club", "Math Club", "Debate Team"
        ]
        
        # Act
        activity_names = list(activities.keys())
        
        # Assert
        assert len(activity_names) == len(expected_activities)
        for activity in expected_activities:
            assert activity in activities


    def test_activity_has_required_fields(self, sample_activity):
        """
        Verify that each activity has all required fields.
        
        AAA Pattern:
        - Arrange: Get a sample activity structure
        - Act: Check for required keys
        - Assert: All required fields are present
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        test_activity = sample_activity
        
        # Act
        activity_keys = test_activity.keys()
        
        # Assert
        for field in required_fields:
            assert field in activity_keys


    def test_activity_participants_is_list(self):
        """
        Verify that participants field in all activities is a list.
        
        AAA Pattern:
        - Arrange: Get all activities
        - Act: Check participants type for each
        - Assert: All participants fields are lists
        """
        # Arrange
        all_activities = activities
        
        # Act & Assert
        for activity_name, activity_data in all_activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"


    def test_activity_max_participants_is_integer(self):
        """
        Verify that max_participants field is an integer for all activities.
        
        AAA Pattern:
        - Arrange: Get all activities
        - Act: Check max_participants type for each
        - Assert: All max_participants are integers
        """
        # Arrange
        all_activities = activities
        
        # Act & Assert
        for activity_name, activity_data in all_activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be integer"
            assert activity_data["max_participants"] > 0, \
                f"{activity_name} max_participants should be positive"


    def test_no_participant_exceeds_max_capacity(self):
        """
        Verify that no activity has more participants than max_participants.
        
        AAA Pattern:
        - Arrange: Get all activities
        - Act: Count participants vs max_participants for each
        - Assert: Participant count never exceeds max capacity
        """
        # Arrange
        all_activities = activities
        
        # Act & Assert
        for activity_name, activity_data in all_activities.items():
            participants_count = len(activity_data["participants"])
            max_participants = activity_data["max_participants"]
            assert participants_count <= max_participants, \
                f"{activity_name} has {participants_count} participants but max is {max_participants}"


    def test_participant_emails_are_strings(self):
        """
        Verify that all participant entries are valid email strings.
        
        AAA Pattern:
        - Arrange: Get all activities and participants
        - Act: Check type and format of each participant
        - Assert: All participants are non-empty strings
        """
        # Arrange
        all_activities = activities
        
        # Act & Assert
        for activity_name, activity_data in all_activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"Participant in {activity_name} should be string, got {type(participant)}"
                assert len(participant) > 0, \
                    f"Participant in {activity_name} should not be empty"
                assert "@" in participant, \
                    f"Participant '{participant}' in {activity_name} should be a valid email"


class TestSignupValidation:
    """Test business logic for signup validation."""
    
    def test_can_detect_duplicate_signup(self, sample_emails):
        """
        Verify logic to detect if a student is already signed up.
        
        AAA Pattern:
        - Arrange: Get a test activity's participants and an existing email
        - Act: Check if existing email is in participants
        - Assert: Duplicate is detected
        """
        # Arrange
        test_activity = activities["Chess Club"]
        existing_email = sample_emails["existing"]
        
        # Act
        is_duplicate = existing_email in test_activity["participants"]
        
        # Assert
        assert is_duplicate is True


    def test_can_detect_new_signup(self, sample_emails):
        """
        Verify logic to detect if a student is NOT yet signed up.
        
        AAA Pattern:
        - Arrange: Get a test activity and a new email not in participants
        - Act: Check if new email is NOT in participants
        - Assert: New signup is detected as eligible
        """
        # Arrange
        test_activity = activities["Chess Club"]
        new_email = sample_emails["new"]
        
        # Act
        is_not_duplicate = new_email not in test_activity["participants"]
        
        # Assert
        assert is_not_duplicate is True


    def test_can_check_capacity_available(self):
        """
        Verify logic to check if activity has available slots.
        
        AAA Pattern:
        - Arrange: Get Math Club which has 1 participant and max 15
        - Act: Calculate available slots
        - Assert: Available slots are correctly calculated
        """
        # Arrange
        activity = activities["Math Club"]
        current_participants = len(activity["participants"])
        max_capacity = activity["max_participants"]
        
        # Act
        available_slots = max_capacity - current_participants
        
        # Assert
        assert available_slots > 0
        assert available_slots == max_capacity - current_participants
