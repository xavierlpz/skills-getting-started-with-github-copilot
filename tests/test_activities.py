"""
Integration tests for FastAPI Activities Management System

Tests cover all endpoints with happy path and error case scenarios:
- GET /activities
- POST /activities/{activity_name}/signup
- DELETE /activities/{activity_name}/signup
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, test_client):
        """Test that GET /activities returns all available activities"""
        response = test_client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9
        
        # Verify all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Swimming Club", "Art Studio", "Drama Club", "Debate Team", "Math Olympiad"
        ]
        for activity in expected_activities:
            assert activity in activities
    
    def test_get_activities_returns_correct_structure(self, test_client):
        """Test that each activity has the expected data structure"""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            # Verify required fields
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            
            # Verify data types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_participants_are_emails(self, test_client):
        """Test that participant list contains valid email addresses"""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_data in activities.values():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successfully_adds_student_to_activity(self, test_client):
        """Test that a new student can successfully sign up for an activity"""
        response = test_client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in response.json()["message"]
        
        # Verify student was added to participants
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_returns_confirmation_message(self, test_client):
        """Test that signup returns appropriate confirmation message"""
        response = test_client.post(
            "/activities/Programming Class/signup",
            params={"email": "john@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "john@mergington.edu" in data["message"]
        assert "Programming Class" in data["message"]
    
    def test_signup_duplicate_email_returns_400_error(self, test_client):
        """Test that signing up an already-enrolled student returns 400 error"""
        # michael@mergington.edu is already in Chess Club
        response = test_client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404_error(self, test_client):
        """Test that signing up for a non-existent activity returns 404 error"""
        response = test_client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_different_activities_different_emails_allowed(self, test_client):
        """Test that a student can sign up for multiple different activities"""
        # Sign up for first activity
        response1 = test_client.post(
            "/activities/Chess Club/signup",
            params={"email": "versatile@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Sign up for second activity with same email
        response2 = test_client.post(
            "/activities/Programming Class/signup",
            params={"email": "versatile@mergington.edu"}
        )
        assert response2.status_code == 200
        
        # Verify student is in both activities
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert "versatile@mergington.edu" in activities["Chess Club"]["participants"]
        assert "versatile@mergington.edu" in activities["Programming Class"]["participants"]


class TestRemoveFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_remove_successfully_removes_student_from_activity(self, test_client):
        """Test that a student can be successfully removed from an activity"""
        # michael@mergington.edu is in Chess Club
        response = test_client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert "michael@mergington.edu" in response.json()["message"]
        
        # Verify student was removed from participants
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_remove_returns_confirmation_message(self, test_client):
        """Test that removal returns appropriate confirmation message"""
        response = test_client.delete(
            "/activities/Programming Class/signup",
            params={"email": "emma@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "emma@mergington.edu" in data["message"]
        assert "Programming Class" in data["message"]
    
    def test_remove_nonexistent_activity_returns_404_error(self, test_client):
        """Test that removing from a non-existent activity returns 404 error"""
        response = test_client.delete(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_student_not_signed_up_returns_400_error(self, test_client):
        """Test that removing a student not in an activity returns 400 error"""
        response = test_client.delete(
            "/activities/Chess Club/signup",
            params={"email": "notstudent@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_remove_after_signup_works_correctly(self, test_client):
        """Test the full flow: sign up, then remove"""
        email = "temporary@mergington.edu"
        
        # Sign up
        signup_response = test_client.post(
            "/activities/Art Studio/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signed up
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Art Studio"]["participants"]
        
        # Remove
        remove_response = test_client.delete(
            "/activities/Art Studio/signup",
            params={"email": email}
        )
        assert remove_response.status_code == 200
        
        # Verify removed
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert email not in activities["Art Studio"]["participants"]


class TestActivityParticipantModifications:
    """Integration tests for participant count and state consistency"""
    
    def test_participant_count_increases_on_signup(self, test_client):
        """Test that participant count increases when signing up"""
        initial_response = test_client.get("/activities")
        initial_count = len(initial_response.json()["Soccer Team"]["participants"])
        
        test_client.post(
            "/activities/Soccer Team/signup",
            params={"email": "newplayer@mergington.edu"}
        )
        
        final_response = test_client.get("/activities")
        final_count = len(final_response.json()["Soccer Team"]["participants"])
        
        assert final_count == initial_count + 1
    
    def test_participant_count_decreases_on_removal(self, test_client):
        """Test that participant count decreases when removing a student"""
        initial_response = test_client.get("/activities")
        initial_count = len(initial_response.json()["Swimming Club"]["participants"])
        
        # Remove an existing participant
        test_client.delete(
            "/activities/Swimming Club/signup",
            params={"email": "lisa@mergington.edu"}
        )
        
        final_response = test_client.get("/activities")
        final_count = len(final_response.json()["Swimming Club"]["participants"])
        
        assert final_count == initial_count - 1
