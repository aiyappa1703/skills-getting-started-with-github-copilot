"""
Integration tests for FastAPI endpoints using AAA (Arrange-Act-Assert) pattern.
Tests the complete API functionality end-to-end.
"""

import pytest


class TestGetActivitiesEndpoint:
    """Test the GET /activities endpoint."""
    
    def test_get_all_activities_returns_200(self, client):
        """
        Verify GET /activities returns a 200 status code.
        
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Make GET request to /activities
        - Assert: Status code is 200 (OK)
        """
        # Arrange
        endpoint = "/activities"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        assert response.status_code == 200


    def test_get_all_activities_returns_json(self, client):
        """
        Verify GET /activities returns JSON content type.
        
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Make GET request and check headers
        - Assert: Content-Type is application/json
        """
        # Arrange
        endpoint = "/activities"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        assert response.headers["content-type"] == "application/json"


    def test_get_all_activities_returns_all_activities(self, client):
        """
        Verify GET /activities returns all activities.
        
        AAA Pattern:
        - Arrange: Expected number of activities
        - Act: Get all activities via endpoint
        - Assert: Response contains expected number of activities
        """
        # Arrange
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data) == expected_activity_count


    def test_get_activities_returns_correct_structure(self, client):
        """
        Verify each activity in the response has required fields.
        
        AAA Pattern:
        - Arrange: Define required fields
        - Act: Get all activities and check structure
        - Assert: Each activity has all required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_details in activities_data.items():
            for field in required_fields:
                assert field in activity_details, \
                    f"Activity '{activity_name}' missing field '{field}'"


    def test_get_activities_includes_chess_club(self, client):
        """
        Verify GET /activities includes specific activity (Chess Club).
        
        AAA Pattern:
        - Arrange: Specify activity to find
        - Act: Get all activities
        - Assert: Chess Club is in the response
        """
        # Arrange
        expected_activity = "Chess Club"
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert expected_activity in data
        assert data[expected_activity]["max_participants"] == 12


class TestSignupForActivityEndpoint:
    """Test the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_student_returns_200(self, client, sample_emails):
        """
        Verify signup for a new student returns 200 status code.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new student email
        - Act: Make POST request to signup endpoint
        - Assert: Status code is 200 (OK)
        """
        # Arrange
        activity_name = "Programming Class"
        email = sample_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200


    def test_signup_new_student_returns_success_message(self, client, sample_emails):
        """
        Verify signup response contains success message.
        
        AAA Pattern:
        - Arrange: Prepare signup data
        - Act: Make signup request
        - Assert: Response contains correct success message
        """
        # Arrange
        activity_name = "Art Studio"
        email = sample_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]


    def test_signup_new_student_adds_to_participants(self, client, sample_emails):
        """
        Verify student is added to activity participants after signup.
        
        AAA Pattern:
        - Arrange: Prepare signup data
        - Act: Sign up student, then get activities
        - Assert: Student appears in participants list
        """
        # Arrange
        activity_name = "Drama Club"
        email = sample_emails["new"]
        
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        participants = activities_data[activity_name]["participants"]
        assert email in participants


    def test_signup_duplicate_student_returns_400(self, client, sample_emails):
        """
        Verify signup for already-registered student returns 400 status.
        
        AAA Pattern:
        - Arrange: Use email of existing participant
        - Act: Attempt to sign up same student again
        - Assert: Status code is 400 (Bad Request)
        """
        # Arrange
        activity_name = "Chess Club"
        email = sample_emails["existing"]  # Already signed up for Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400


    def test_signup_duplicate_student_returns_error(self, client, sample_emails):
        """
        Verify error message for duplicate signup.
        
        AAA Pattern:
        - Arrange: Prepare duplicate signup attempt
        - Act: Attempt signup and get response
        - Assert: Error message indicates student already signed up
        """
        # Arrange
        activity_name = "Chess Club"
        email = sample_emails["existing"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()


    def test_signup_nonexistent_activity_returns_404(self, client, sample_emails):
        """
        Verify signup for non-existent activity returns 404 status.
        
        AAA Pattern:
        - Arrange: Use invalid activity name
        - Act: Attempt to sign up for non-existent activity
        - Assert: Status code is 404 (Not Found)
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = sample_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404


    def test_signup_nonexistent_activity_returns_error(self, client, sample_emails):
        """
        Verify error message for signup to non-existent activity.
        
        AAA Pattern:
        - Arrange: Prepare signup to non-existent activity
        - Act: Make signup request
        - Assert: Error indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = sample_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestUnregisterFromActivityEndpoint:
    """Test the DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_unregister_existing_student_returns_200(self, client, sample_emails):
        """
        Verify unregister for signed-up student returns 200 status.
        
        AAA Pattern:
        - Arrange: Sign up a student first
        - Act: Unregister the student
        - Assert: Status code is 200 (OK)
        """
        # Arrange
        activity_name = "Math Club"
        email = sample_emails["new"]
        
        # First sign them up
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200


    def test_unregister_removes_from_participants(self, client, sample_emails):
        """
        Verify student is removed from participants after unregister.
        
        AAA Pattern:
        - Arrange: Sign up a student
        - Act: Unregister, then get activities
        - Assert: Student no longer in participants list
        """
        # Arrange
        activity_name = "Debate Team"
        email = sample_emails["new"]
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Act
        client.delete(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        participants = activities_data[activity_name]["participants"]
        assert email not in participants


    def test_unregister_nonexistent_student_returns_400(self, client, sample_emails):
        """
        Verify unregister for non-registered student returns 400.
        
        AAA Pattern:
        - Arrange: Use email not signed up for activity
        - Act: Attempt to unregister
        - Assert: Status code is 400 (Bad Request)
        """
        # Arrange
        activity_name = "Basketball Team"
        email = sample_emails["new"]  # Not signed up for Basketball Team
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400


    def test_unregister_nonexistent_student_returns_error(self, client, sample_emails):
        """
        Verify error message when unregistering non-registered student.
        
        AAA Pattern:
        - Arrange: Prepare unregister for non-registered student
        - Act: Make delete request
        - Assert: Error indicates student not signed up
        """
        # Arrange
        activity_name = "Basketball Team"
        email = sample_emails["new"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()


    def test_unregister_from_nonexistent_activity_returns_404(self, client, sample_emails):
        """
        Verify unregister from non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Use invalid activity name
        - Act: Attempt to unregister from non-existent activity
        - Assert: Status code is 404 (Not Found)
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = sample_emails["existing"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404


class TestRootEndpoint:
    """Test the GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Verify root endpoint redirects to static index.html.
        
        AAA Pattern:
        - Arrange: Prepare test client
        - Act: Make GET request to root endpoint (follow_redirects=False)
        - Assert: Response is a redirect (307) to /static/index.html
        """
        # Arrange
        endpoint = "/"
        
        # Act
        response = client.get(endpoint, follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
