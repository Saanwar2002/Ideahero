#!/usr/bin/env python3
"""
Backend API Testing for IdeaHero.com
Tests user authentication, idea validation system, voting, and comments
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Load backend URL from frontend .env
BACKEND_URL = "https://d3f49592-8bfd-4c9e-805c-9412e4dd74fd.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_id = None
        self.submitted_idea_id = None  # For idea submission tests
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Hello World":
                    self.log_test("Basic API Connectivity", True, "API root endpoint responding correctly")
                    return True
                else:
                    self.log_test("Basic API Connectivity", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Basic API Connectivity", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Basic API Connectivity", False, f"Connection error: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test user registration with valid data"""
        try:
            # Generate unique email for testing
            timestamp = int(time.time())
            test_data = {
                "email": f"sarah.johnson{timestamp}@techstartup.com",
                "password": "SecurePass123!",
                "full_name": "Sarah Johnson",
                "skills": ["Python", "React", "Machine Learning", "Product Management"],
                "interests": ["AI/ML", "FinTech", "SaaS", "Mobile Apps"],
                "experience_level": "intermediate"
            }
            
            response = self.session.post(f"{self.base_url}/auth/register", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if all(key in data for key in ["access_token", "token_type", "user"]):
                    self.auth_token = data["access_token"]
                    self.test_user_id = data["user"]["id"]
                    user_data = data["user"]
                    
                    # Verify user data
                    if (user_data["email"] == test_data["email"] and 
                        user_data["full_name"] == test_data["full_name"] and
                        user_data["skills"] == test_data["skills"] and
                        user_data["interests"] == test_data["interests"] and
                        user_data["experience_level"] == test_data["experience_level"] and
                        user_data["reputation_score"] == 0):
                        
                        self.log_test("User Registration", True, 
                                    f"User registered successfully with ID: {self.test_user_id}")
                        return True
                    else:
                        self.log_test("User Registration", False, "User data mismatch in response")
                        return False
                else:
                    self.log_test("User Registration", False, f"Missing required fields in response: {data}")
                    return False
            else:
                self.log_test("User Registration", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Registration", False, f"Exception: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login with correct credentials"""
        try:
            # First register a new user for login test
            timestamp = int(time.time()) + 1  # Different timestamp
            register_data = {
                "email": f"john.doe{timestamp}@startup.com",
                "password": "LoginTest123!",
                "full_name": "John Doe",
                "skills": ["JavaScript", "Node.js"],
                "interests": ["Web Development"]
            }
            
            # Register the user first
            reg_response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
            if reg_response.status_code != 200:
                self.log_test("User Login", False, f"Failed to register test user: {reg_response.status_code}")
                return False
            
            # Now test login with the same credentials
            login_data = {
                "email": register_data["email"],
                "password": register_data["password"]
            }
            
            response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if all(key in data for key in ["access_token", "token_type", "user"]):
                    self.log_test("User Login", True, "Login successful with valid credentials")
                    return True
                else:
                    self.log_test("User Login", False, f"Missing required fields: {data}")
                    return False
            else:
                self.log_test("User Login", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Login", False, f"Exception: {str(e)}")
            return False
    
    def test_authentication_token_validation(self):
        """Test JWT token validation"""
        try:
            if not self.auth_token:
                self.log_test("Token Validation", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(f"{self.base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data and "email" in data and "full_name" in data:
                    self.log_test("Token Validation", True, f"Token validated successfully for user: {data['full_name']}")
                    return True
                else:
                    self.log_test("Token Validation", False, f"Invalid user data structure: {data}")
                    return False
            else:
                self.log_test("Token Validation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_profile_updates(self):
        """Test profile update functionality"""
        try:
            if not self.auth_token:
                self.log_test("Profile Update", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            update_data = {
                "full_name": "Sarah Johnson-Smith",
                "skills": ["Python", "React", "Machine Learning", "Product Management", "DevOps"],
                "interests": ["AI/ML", "FinTech", "SaaS", "Mobile Apps", "Blockchain"],
                "experience_level": "advanced"
            }
            
            response = self.session.put(f"{self.base_url}/auth/profile", 
                                      json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if (data["full_name"] == update_data["full_name"] and
                    data["skills"] == update_data["skills"] and
                    data["interests"] == update_data["interests"] and
                    data["experience_level"] == update_data["experience_level"]):
                    
                    self.log_test("Profile Update", True, "Profile updated successfully")
                    return True
                else:
                    self.log_test("Profile Update", False, f"Profile data mismatch: {data}")
                    return False
            else:
                self.log_test("Profile Update", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Profile Update", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_ideas_api(self):
        """Test fetching enhanced ideas with validation scores"""
        try:
            response = self.session.get(f"{self.base_url}/ideas")
            
            if response.status_code == 200:
                ideas = response.json()
                if isinstance(ideas, list):
                    if len(ideas) > 0:
                        # Check first idea structure
                        idea = ideas[0]
                        required_fields = ["id", "title", "description", "category", "validation_score", 
                                         "total_votes", "avg_feasibility", "avg_market_potential", "avg_interest"]
                        
                        if all(field in idea for field in required_fields):
                            self.log_test("Enhanced Ideas API", True, 
                                        f"Retrieved {len(ideas)} ideas with validation scores")
                            return True
                        else:
                            missing = [f for f in required_fields if f not in idea]
                            self.log_test("Enhanced Ideas API", False, f"Missing fields: {missing}")
                            return False
                    else:
                        self.log_test("Enhanced Ideas API", False, "No ideas returned from database")
                        return False
                else:
                    self.log_test("Enhanced Ideas API", False, f"Expected list, got: {type(ideas)}")
                    return False
            else:
                self.log_test("Enhanced Ideas API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Ideas API", False, f"Exception: {str(e)}")
            return False
    
    def test_ideas_filtering_sorting(self):
        """Test ideas filtering by category and sorting"""
        try:
            # Test filtering by category
            response = self.session.get(f"{self.base_url}/ideas?category=Technology")
            if response.status_code == 200:
                tech_ideas = response.json()
                
                # Test sorting by validation_score (default)
                response2 = self.session.get(f"{self.base_url}/ideas?sort_by=validation_score")
                if response2.status_code == 200:
                    sorted_ideas = response2.json()
                    
                    # Test sorting by created_at
                    response3 = self.session.get(f"{self.base_url}/ideas?sort_by=created_at")
                    if response3.status_code == 200:
                        time_sorted = response3.json()
                        
                        self.log_test("Ideas Filtering & Sorting", True, 
                                    f"Filtering and sorting working - Tech: {len(tech_ideas)}, "
                                    f"Score sorted: {len(sorted_ideas)}, Time sorted: {len(time_sorted)}")
                        return True
                    else:
                        self.log_test("Ideas Filtering & Sorting", False, "Time sorting failed")
                        return False
                else:
                    self.log_test("Ideas Filtering & Sorting", False, "Score sorting failed")
                    return False
            else:
                self.log_test("Ideas Filtering & Sorting", False, f"Category filtering failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Ideas Filtering & Sorting", False, f"Exception: {str(e)}")
            return False
    
    def test_single_idea_details(self):
        """Test single idea details endpoint"""
        try:
            # First get list of ideas to get an ID
            response = self.session.get(f"{self.base_url}/ideas?limit=1")
            if response.status_code == 200:
                ideas = response.json()
                if len(ideas) > 0:
                    idea_id = ideas[0]["id"]
                    
                    # Test single idea endpoint
                    response2 = self.session.get(f"{self.base_url}/ideas/{idea_id}")
                    if response2.status_code == 200:
                        idea = response2.json()
                        if idea["id"] == idea_id:
                            self.log_test("Single Idea Details", True, f"Retrieved idea: {idea['title']}")
                            return True
                        else:
                            self.log_test("Single Idea Details", False, "ID mismatch in response")
                            return False
                    else:
                        self.log_test("Single Idea Details", False, f"HTTP {response2.status_code}")
                        return False
                else:
                    self.log_test("Single Idea Details", False, "No ideas available for testing")
                    return False
            else:
                self.log_test("Single Idea Details", False, "Could not fetch ideas list")
                return False
                
        except Exception as e:
            self.log_test("Single Idea Details", False, f"Exception: {str(e)}")
            return False
    
    def test_idea_voting_system(self):
        """Test voting on ideas with feasibility, market_potential, interest scores"""
        try:
            if not self.auth_token:
                self.log_test("Idea Voting System", False, "No auth token available")
                return False
            
            # Get an idea to vote on
            response = self.session.get(f"{self.base_url}/ideas?limit=1")
            if response.status_code != 200 or not response.json():
                self.log_test("Idea Voting System", False, "No ideas available for voting")
                return False
            
            idea_id = response.json()[0]["id"]
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Test voting
            vote_data = {
                "idea_id": idea_id,
                "vote_type": "upvote",
                "feasibility_score": 4,
                "market_potential_score": 5,
                "interest_score": 4
            }
            
            response = self.session.post(f"{self.base_url}/ideas/{idea_id}/vote", 
                                       json=vote_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "scores" in data:
                    scores = data["scores"]
                    if all(key in scores for key in ["validation_score", "total_votes", "avg_feasibility"]):
                        self.log_test("Idea Voting System", True, 
                                    f"Vote recorded successfully. New validation score: {scores['validation_score']}")
                        
                        # Test updating existing vote
                        updated_vote = {
                            "idea_id": idea_id,
                            "vote_type": "upvote",
                            "feasibility_score": 5,
                            "market_potential_score": 4,
                            "interest_score": 5
                        }
                        
                        response2 = self.session.post(f"{self.base_url}/ideas/{idea_id}/vote", 
                                                    json=updated_vote, headers=headers)
                        
                        if response2.status_code == 200:
                            self.log_test("Vote Update", True, "Existing vote updated successfully")
                            return True
                        else:
                            self.log_test("Vote Update", False, f"Vote update failed: {response2.status_code}")
                            return False
                    else:
                        self.log_test("Idea Voting System", False, f"Missing score fields: {scores}")
                        return False
                else:
                    self.log_test("Idea Voting System", False, f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Idea Voting System", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Idea Voting System", False, f"Exception: {str(e)}")
            return False
    
    def test_comment_system(self):
        """Test adding comments to ideas"""
        try:
            if not self.auth_token:
                self.log_test("Comment System", False, "No auth token available")
                return False
            
            # Get an idea to comment on
            response = self.session.get(f"{self.base_url}/ideas?limit=1")
            if response.status_code != 200 or not response.json():
                self.log_test("Comment System", False, "No ideas available for commenting")
                return False
            
            idea_id = response.json()[0]["id"]
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Test adding comment
            comment_data = {
                "idea_id": idea_id,
                "content": "This is a fantastic idea! I've been working on something similar in the fintech space and I think there's huge market potential here. The implementation approach you've outlined seems very feasible."
            }
            
            response = self.session.post(f"{self.base_url}/ideas/{idea_id}/comment", 
                                       json=comment_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "comment" in data:
                    comment = data["comment"]
                    if (comment["content"] == comment_data["content"] and
                        "user_name" in comment and
                        "created_at" in comment):
                        
                        self.log_test("Comment System", True, "Comment added successfully with user info")
                        
                        # Test comment validation (minimum length)
                        short_comment = {
                            "idea_id": idea_id,
                            "content": "Too short"
                        }
                        
                        response2 = self.session.post(f"{self.base_url}/ideas/{idea_id}/comment", 
                                                    json=short_comment, headers=headers)
                        
                        if response2.status_code == 400:
                            self.log_test("Comment Validation", True, "Short comment properly rejected")
                            return True
                        else:
                            self.log_test("Comment Validation", False, "Short comment validation failed")
                            return False
                    else:
                        self.log_test("Comment System", False, f"Invalid comment structure: {comment}")
                        return False
                else:
                    self.log_test("Comment System", False, f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Comment System", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Comment System", False, f"Exception: {str(e)}")
            return False
    
    def test_authentication_requirements(self):
        """Test that protected endpoints require authentication"""
        try:
            # Test accessing protected endpoint without token
            response = self.session.get(f"{self.base_url}/auth/me")
            
            if response.status_code in [401, 403]:  # Both are acceptable for unauthorized access
                self.log_test("Authentication Requirements", True, 
                            f"Protected endpoints properly require authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("Authentication Requirements", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Authentication Requirements", False, f"Exception: {str(e)}")
            return False
    
    def test_input_validation(self):
        """Test input validation for endpoints"""
        try:
            # Test invalid email registration
            invalid_data = {
                "email": "invalid-email",
                "password": "123",  # Too short
                "full_name": "Test User"
            }
            
            response = self.session.post(f"{self.base_url}/auth/register", json=invalid_data)
            
            if response.status_code in [400, 422]:  # Both are acceptable for validation errors
                self.log_test("Input Validation", True, 
                            f"Invalid input properly rejected (HTTP {response.status_code})")
                return True
            else:
                self.log_test("Input Validation", False, 
                            f"Expected 400/422 for invalid input, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Input Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_user_dashboard_authentication(self):
        """Test that user dashboard endpoint requires authentication"""
        try:
            # Test without authentication
            response = self.session.get(f"{self.base_url}/user/dashboard")
            
            if response.status_code in [401, 403]:
                self.log_test("User Dashboard Authentication", True, 
                            f"Dashboard properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("User Dashboard Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User Dashboard Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_user_dashboard_data(self):
        """Test user dashboard endpoint returns comprehensive user stats"""
        try:
            if not self.auth_token:
                self.log_test("User Dashboard Data", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(f"{self.base_url}/user/dashboard", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required top-level structure
                required_sections = ["user_stats", "recent_activity", "engagement_summary"]
                if not all(section in data for section in required_sections):
                    missing = [s for s in required_sections if s not in data]
                    self.log_test("User Dashboard Data", False, f"Missing sections: {missing}")
                    return False
                
                # Check user_stats structure
                user_stats = data["user_stats"]
                required_stats = ["total_votes", "total_comments", "upvotes_given", "downvotes_given", 
                                "reputation_score", "member_since", "favorite_categories"]
                if not all(stat in user_stats for stat in required_stats):
                    missing = [s for s in required_stats if s not in user_stats]
                    self.log_test("User Dashboard Data", False, f"Missing user stats: {missing}")
                    return False
                
                # Check recent_activity structure
                recent_activity = data["recent_activity"]
                required_activity = ["voted_ideas", "commented_ideas"]
                if not all(activity in recent_activity for activity in required_activity):
                    missing = [a for a in required_activity if a not in recent_activity]
                    self.log_test("User Dashboard Data", False, f"Missing activity data: {missing}")
                    return False
                
                # Check engagement_summary structure
                engagement = data["engagement_summary"]
                required_engagement = ["total_interactions", "vote_ratio", "active_days"]
                if not all(metric in engagement for metric in required_engagement):
                    missing = [m for m in required_engagement if m not in engagement]
                    self.log_test("User Dashboard Data", False, f"Missing engagement metrics: {missing}")
                    return False
                
                # Verify data types and values
                if (isinstance(user_stats["total_votes"], int) and
                    isinstance(user_stats["total_comments"], int) and
                    isinstance(user_stats["reputation_score"], int) and
                    isinstance(user_stats["favorite_categories"], list) and
                    isinstance(recent_activity["voted_ideas"], list) and
                    isinstance(recent_activity["commented_ideas"], list) and
                    isinstance(engagement["total_interactions"], int)):
                    
                    self.log_test("User Dashboard Data", True, 
                                f"Dashboard data structure valid - {user_stats['total_votes']} votes, "
                                f"{user_stats['total_comments']} comments, "
                                f"reputation: {user_stats['reputation_score']}")
                    return True
                else:
                    self.log_test("User Dashboard Data", False, "Invalid data types in response")
                    return False
            else:
                self.log_test("User Dashboard Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Dashboard Data", False, f"Exception: {str(e)}")
            return False
    
    def test_user_analytics_authentication(self):
        """Test that user analytics endpoint requires authentication"""
        try:
            # Test without authentication
            response = self.session.get(f"{self.base_url}/user/analytics")
            
            if response.status_code in [401, 403]:
                self.log_test("User Analytics Authentication", True, 
                            f"Analytics properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("User Analytics Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User Analytics Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_user_analytics_data(self):
        """Test user analytics endpoint returns chart-ready data"""
        try:
            if not self.auth_token:
                self.log_test("User Analytics Data", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(f"{self.base_url}/user/analytics", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required structure for analytics
                required_fields = ["activity_timeline", "category_distribution", "score_distribution", "total_interactions"]
                if not all(field in data for field in required_fields):
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("User Analytics Data", False, f"Missing analytics fields: {missing}")
                    return False
                
                # Verify data structure for charts
                activity_timeline = data["activity_timeline"]
                category_distribution = data["category_distribution"]
                score_distribution = data["score_distribution"]
                
                # Check that timeline data has proper structure
                if isinstance(activity_timeline, list):
                    if len(activity_timeline) > 0:
                        timeline_item = activity_timeline[0]
                        required_timeline_fields = ["month", "votes", "comments", "total"]
                        if not all(field in timeline_item for field in required_timeline_fields):
                            missing = [f for f in required_timeline_fields if f not in timeline_item]
                            self.log_test("User Analytics Data", False, f"Missing timeline fields: {missing}")
                            return False
                
                # Check category distribution structure
                if isinstance(category_distribution, list):
                    if len(category_distribution) > 0:
                        cat_item = category_distribution[0]
                        if not ("category" in cat_item and "count" in cat_item):
                            self.log_test("User Analytics Data", False, "Invalid category distribution structure")
                            return False
                
                # Check score distribution structure
                if isinstance(score_distribution, list):
                    if len(score_distribution) > 0:
                        score_item = score_distribution[0]
                        if not ("score" in score_item and "count" in score_item):
                            self.log_test("User Analytics Data", False, "Invalid score distribution structure")
                            return False
                
                # Verify total_interactions is a number
                if isinstance(data["total_interactions"], int):
                    self.log_test("User Analytics Data", True, 
                                f"Analytics data structure valid - {len(activity_timeline)} timeline entries, "
                                f"{len(category_distribution)} categories, "
                                f"{data['total_interactions']} total interactions")
                    return True
                else:
                    self.log_test("User Analytics Data", False, "Invalid total_interactions type")
                    return False
            else:
                self.log_test("User Analytics Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Analytics Data", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_analytics_integration(self):
        """Test that dashboard and analytics data is consistent"""
        try:
            if not self.auth_token:
                self.log_test("Dashboard Analytics Integration", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Get both dashboard and analytics data
            dashboard_response = self.session.get(f"{self.base_url}/user/dashboard", headers=headers)
            analytics_response = self.session.get(f"{self.base_url}/user/analytics", headers=headers)
            
            if dashboard_response.status_code == 200 and analytics_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                analytics_data = analytics_response.json()
                
                # Check that total interactions match between dashboard and analytics
                dashboard_interactions = dashboard_data["engagement_summary"]["total_interactions"]
                analytics_interactions = analytics_data["total_interactions"]
                
                if dashboard_interactions == analytics_interactions:
                    self.log_test("Dashboard Analytics Integration", True, 
                                f"Data consistency verified - {dashboard_interactions} total interactions")
                    return True
                else:
                    self.log_test("Dashboard Analytics Integration", False, 
                                f"Interaction count mismatch - Dashboard: {dashboard_interactions}, "
                                f"Analytics: {analytics_interactions}")
                    return False
            else:
                self.log_test("Dashboard Analytics Integration", False, 
                            f"Failed to fetch data - Dashboard: {dashboard_response.status_code}, "
                            f"Analytics: {analytics_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Analytics Integration", False, f"Exception: {str(e)}")
            return False

    # ===== IDEA SUBMISSION SYSTEM TESTS =====
    
    def test_idea_submission_authentication(self):
        """Test that idea submission requires authentication"""
        try:
            # Test without authentication
            idea_data = {
                "title": "Test Idea",
                "description": "This is a test idea",
                "category": "Technology"
            }
            
            response = self.session.post(f"{self.base_url}/ideas/submit", json=idea_data)
            
            if response.status_code in [401, 403]:
                self.log_test("Idea Submission Authentication", True, 
                            f"Idea submission properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("Idea Submission Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Idea Submission Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_idea_submission_valid_data(self):
        """Test idea submission with valid data"""
        try:
            if not self.auth_token:
                self.log_test("Idea Submission Valid Data", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Test comprehensive idea submission
            idea_data = {
                "title": "AI-Powered Personal Finance Assistant",
                "description": "A comprehensive personal finance management app that uses AI to analyze spending patterns, predict future expenses, and provide personalized budgeting recommendations. The app would integrate with multiple bank accounts and credit cards to provide real-time financial insights.",
                "category": "FinTech",
                "tags": ["AI", "Machine Learning", "Personal Finance", "Mobile App", "Banking Integration"],
                "target_market": "Young professionals aged 25-40 who want better control over their finances",
                "problem_statement": "Many people struggle to manage their finances effectively due to lack of visibility into spending patterns and difficulty creating realistic budgets",
                "solution_approach": "Use machine learning algorithms to analyze transaction data and provide actionable insights through an intuitive mobile interface",
                "business_model": "Freemium model with basic features free and premium analytics for $9.99/month",
                "competitive_advantage": "Advanced AI algorithms and seamless integration with multiple financial institutions"
            }
            
            response = self.session.post(f"{self.base_url}/ideas/submit", json=idea_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["id", "title", "description", "category", "submitter_id", "submitter_name", "status", "created_at"]
                if not all(field in data for field in required_fields):
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Idea Submission Valid Data", False, f"Missing response fields: {missing}")
                    return False
                
                # Verify data accuracy
                if (data["title"] == idea_data["title"] and
                    data["description"] == idea_data["description"] and
                    data["category"] == idea_data["category"] and
                    data["tags"] == idea_data["tags"] and
                    data["status"] == "pending"):
                    
                    # Store the submitted idea ID for later tests
                    self.submitted_idea_id = data["id"]
                    
                    self.log_test("Idea Submission Valid Data", True, 
                                f"Idea submitted successfully with ID: {data['id']}, Status: {data['status']}")
                    return True
                else:
                    self.log_test("Idea Submission Valid Data", False, "Data mismatch in response")
                    return False
            else:
                self.log_test("Idea Submission Valid Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Idea Submission Valid Data", False, f"Exception: {str(e)}")
            return False
    
    def test_idea_submission_reputation_increase(self):
        """Test that submitting an idea increases reputation by 5 points"""
        try:
            if not self.auth_token:
                self.log_test("Idea Submission Reputation Increase", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Get current reputation
            profile_response = self.session.get(f"{self.base_url}/auth/me", headers=headers)
            if profile_response.status_code != 200:
                self.log_test("Idea Submission Reputation Increase", False, "Could not get current reputation")
                return False
            
            initial_reputation = profile_response.json()["reputation_score"]
            
            # Submit another idea
            idea_data = {
                "title": "Smart Home Energy Optimization System",
                "description": "An IoT-based system that learns household energy usage patterns and automatically optimizes energy consumption to reduce costs and environmental impact.",
                "category": "Technology",
                "tags": ["IoT", "Smart Home", "Energy", "Sustainability"],
                "target_market": "Homeowners interested in reducing energy costs",
                "problem_statement": "High energy bills and inefficient energy usage in homes",
                "solution_approach": "Smart sensors and AI algorithms to optimize energy consumption"
            }
            
            response = self.session.post(f"{self.base_url}/ideas/submit", json=idea_data, headers=headers)
            
            if response.status_code == 200:
                # Check reputation after submission
                profile_response2 = self.session.get(f"{self.base_url}/auth/me", headers=headers)
                if profile_response2.status_code == 200:
                    new_reputation = profile_response2.json()["reputation_score"]
                    reputation_increase = new_reputation - initial_reputation
                    
                    if reputation_increase == 5:
                        self.log_test("Idea Submission Reputation Increase", True, 
                                    f"Reputation increased by {reputation_increase} points (from {initial_reputation} to {new_reputation})")
                        return True
                    else:
                        self.log_test("Idea Submission Reputation Increase", False, 
                                    f"Expected +5 reputation, got +{reputation_increase}")
                        return False
                else:
                    self.log_test("Idea Submission Reputation Increase", False, "Could not verify new reputation")
                    return False
            else:
                self.log_test("Idea Submission Reputation Increase", False, f"Idea submission failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Idea Submission Reputation Increase", False, f"Exception: {str(e)}")
            return False
    
    def test_user_submitted_ideas_authentication(self):
        """Test that getting user's submitted ideas requires authentication"""
        try:
            # Test without authentication
            response = self.session.get(f"{self.base_url}/ideas/submitted")
            
            if response.status_code in [401, 403]:
                self.log_test("User Submitted Ideas Authentication", True, 
                            f"User submitted ideas properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("User Submitted Ideas Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User Submitted Ideas Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_user_submitted_ideas_data(self):
        """Test getting user's submitted ideas returns correct data"""
        try:
            if not self.auth_token:
                self.log_test("User Submitted Ideas Data", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(f"{self.base_url}/ideas/submitted", headers=headers)
            
            if response.status_code == 200:
                ideas = response.json()
                
                if isinstance(ideas, list):
                    if len(ideas) > 0:
                        # Check that all ideas belong to current user
                        user_response = self.session.get(f"{self.base_url}/auth/me", headers=headers)
                        if user_response.status_code == 200:
                            current_user_id = user_response.json()["id"]
                            
                            all_user_ideas = all(idea["submitter_id"] == current_user_id for idea in ideas)
                            if all_user_ideas:
                                self.log_test("User Submitted Ideas Data", True, 
                                            f"Retrieved {len(ideas)} user-submitted ideas correctly")
                                return True
                            else:
                                self.log_test("User Submitted Ideas Data", False, 
                                            "Some ideas don't belong to current user")
                                return False
                        else:
                            self.log_test("User Submitted Ideas Data", False, "Could not verify current user")
                            return False
                    else:
                        self.log_test("User Submitted Ideas Data", True, "No submitted ideas found (empty response is valid)")
                        return True
                else:
                    self.log_test("User Submitted Ideas Data", False, f"Expected list, got {type(ideas)}")
                    return False
            else:
                self.log_test("User Submitted Ideas Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Submitted Ideas Data", False, f"Exception: {str(e)}")
            return False
    
    def test_submitted_idea_details_authentication(self):
        """Test that getting submitted idea details requires authentication and ownership"""
        try:
            if not hasattr(self, 'submitted_idea_id'):
                self.log_test("Submitted Idea Details Authentication", False, "No submitted idea ID available")
                return False
            
            # Test without authentication
            response = self.session.get(f"{self.base_url}/ideas/submitted/{self.submitted_idea_id}")
            
            if response.status_code in [401, 403]:
                self.log_test("Submitted Idea Details Authentication", True, 
                            f"Submitted idea details properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("Submitted Idea Details Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Submitted Idea Details Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_submitted_idea_details_data(self):
        """Test getting submitted idea details returns correct data"""
        try:
            if not self.auth_token or not hasattr(self, 'submitted_idea_id'):
                self.log_test("Submitted Idea Details Data", False, "No auth token or submitted idea ID available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(f"{self.base_url}/ideas/submitted/{self.submitted_idea_id}", headers=headers)
            
            if response.status_code == 200:
                idea = response.json()
                
                # Verify idea structure
                required_fields = ["id", "title", "description", "category", "submitter_id", "status", "created_at"]
                if not all(field in idea for field in required_fields):
                    missing = [f for f in required_fields if f not in idea]
                    self.log_test("Submitted Idea Details Data", False, f"Missing fields: {missing}")
                    return False
                
                # Verify this is the correct idea
                if idea["id"] == self.submitted_idea_id:
                    self.log_test("Submitted Idea Details Data", True, 
                                f"Retrieved idea details correctly: {idea['title']}")
                    return True
                else:
                    self.log_test("Submitted Idea Details Data", False, "ID mismatch in response")
                    return False
            else:
                self.log_test("Submitted Idea Details Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Submitted Idea Details Data", False, f"Exception: {str(e)}")
            return False
    
    def test_submitted_idea_details_404(self):
        """Test 404 error for non-existent submitted ideas"""
        try:
            if not self.auth_token:
                self.log_test("Submitted Idea Details 404", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            fake_id = "non-existent-idea-id-12345"
            response = self.session.get(f"{self.base_url}/ideas/submitted/{fake_id}", headers=headers)
            
            if response.status_code == 404:
                self.log_test("Submitted Idea Details 404", True, "Non-existent idea properly returns 404")
                return True
            else:
                self.log_test("Submitted Idea Details 404", False, f"Expected 404, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Submitted Idea Details 404", False, f"Exception: {str(e)}")
            return False
    
    def test_update_submitted_idea_authentication(self):
        """Test that updating submitted ideas requires authentication"""
        try:
            if not hasattr(self, 'submitted_idea_id'):
                self.log_test("Update Submitted Idea Authentication", False, "No submitted idea ID available")
                return False
            
            # Test without authentication
            update_data = {
                "title": "Updated Title",
                "description": "Updated description",
                "category": "Technology"
            }
            
            response = self.session.put(f"{self.base_url}/ideas/submitted/{self.submitted_idea_id}", json=update_data)
            
            if response.status_code in [401, 403]:
                self.log_test("Update Submitted Idea Authentication", True, 
                            f"Update submitted idea properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("Update Submitted Idea Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Update Submitted Idea Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_update_submitted_idea_valid(self):
        """Test updating a pending submitted idea"""
        try:
            if not self.auth_token or not hasattr(self, 'submitted_idea_id'):
                self.log_test("Update Submitted Idea Valid", False, "No auth token or submitted idea ID available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Update the idea
            update_data = {
                "title": "AI-Powered Personal Finance Assistant (Updated)",
                "description": "An enhanced comprehensive personal finance management app that uses advanced AI to analyze spending patterns, predict future expenses, and provide personalized budgeting recommendations with real-time alerts.",
                "category": "FinTech",
                "tags": ["AI", "Machine Learning", "Personal Finance", "Mobile App", "Banking Integration", "Real-time Alerts"],
                "target_market": "Young professionals and families aged 25-45 who want better control over their finances",
                "business_model": "Freemium model with basic features free and premium analytics for $12.99/month"
            }
            
            response = self.session.put(f"{self.base_url}/ideas/submitted/{self.submitted_idea_id}", 
                                      json=update_data, headers=headers)
            
            if response.status_code == 200:
                updated_idea = response.json()
                
                # Verify the update
                if (updated_idea["title"] == update_data["title"] and
                    updated_idea["description"] == update_data["description"] and
                    updated_idea["business_model"] == update_data["business_model"] and
                    "updated_at" in updated_idea):
                    
                    self.log_test("Update Submitted Idea Valid", True, 
                                f"Idea updated successfully: {updated_idea['title']}")
                    return True
                else:
                    self.log_test("Update Submitted Idea Valid", False, "Update data mismatch")
                    return False
            else:
                self.log_test("Update Submitted Idea Valid", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Update Submitted Idea Valid", False, f"Exception: {str(e)}")
            return False
    
    def test_delete_submitted_idea_authentication(self):
        """Test that deleting submitted ideas requires authentication"""
        try:
            # Create a new idea for deletion test
            if not self.auth_token:
                self.log_test("Delete Submitted Idea Authentication", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # First create an idea to delete
            idea_data = {
                "title": "Test Idea for Deletion",
                "description": "This idea will be deleted in the test",
                "category": "Technology"
            }
            
            create_response = self.session.post(f"{self.base_url}/ideas/submit", json=idea_data, headers=headers)
            if create_response.status_code != 200:
                self.log_test("Delete Submitted Idea Authentication", False, "Could not create test idea")
                return False
            
            delete_idea_id = create_response.json()["id"]
            
            # Test deletion without authentication
            response = self.session.delete(f"{self.base_url}/ideas/submitted/{delete_idea_id}")
            
            if response.status_code in [401, 403]:
                self.log_test("Delete Submitted Idea Authentication", True, 
                            f"Delete submitted idea properly requires authentication (HTTP {response.status_code})")
                return True
            else:
                self.log_test("Delete Submitted Idea Authentication", False, 
                            f"Expected 401/403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Delete Submitted Idea Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_delete_submitted_idea_valid(self):
        """Test deleting a pending submitted idea"""
        try:
            if not self.auth_token:
                self.log_test("Delete Submitted Idea Valid", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            # Create an idea to delete
            idea_data = {
                "title": "Temporary Idea for Deletion Test",
                "description": "This idea will be deleted to test the deletion functionality",
                "category": "Technology"
            }
            
            create_response = self.session.post(f"{self.base_url}/ideas/submit", json=idea_data, headers=headers)
            if create_response.status_code != 200:
                self.log_test("Delete Submitted Idea Valid", False, "Could not create test idea")
                return False
            
            delete_idea_id = create_response.json()["id"]
            
            # Delete the idea
            response = self.session.delete(f"{self.base_url}/ideas/submitted/{delete_idea_id}", headers=headers)
            
            if response.status_code == 200:
                # Verify deletion by trying to get the idea
                get_response = self.session.get(f"{self.base_url}/ideas/submitted/{delete_idea_id}", headers=headers)
                
                if get_response.status_code == 404:
                    self.log_test("Delete Submitted Idea Valid", True, "Idea deleted successfully and returns 404")
                    return True
                else:
                    self.log_test("Delete Submitted Idea Valid", False, 
                                f"Idea still exists after deletion (HTTP {get_response.status_code})")
                    return False
            else:
                self.log_test("Delete Submitted Idea Valid", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Delete Submitted Idea Valid", False, f"Exception: {str(e)}")
            return False
    
    def test_community_ideas_endpoint(self):
        """Test community ideas endpoint returns only approved ideas"""
        try:
            response = self.session.get(f"{self.base_url}/ideas/community")
            
            if response.status_code == 200:
                ideas = response.json()
                
                if isinstance(ideas, list):
                    # Check that all returned ideas are approved (if any exist)
                    if len(ideas) > 0:
                        all_approved = all(idea.get("status") == "approved" for idea in ideas)
                        if all_approved:
                            self.log_test("Community Ideas Endpoint", True, 
                                        f"Retrieved {len(ideas)} approved community ideas")
                            return True
                        else:
                            non_approved = [idea for idea in ideas if idea.get("status") != "approved"]
                            self.log_test("Community Ideas Endpoint", False, 
                                        f"Found {len(non_approved)} non-approved ideas in community feed")
                            return False
                    else:
                        self.log_test("Community Ideas Endpoint", True, "No community ideas found (empty response is valid)")
                        return True
                else:
                    self.log_test("Community Ideas Endpoint", False, f"Expected list, got {type(ideas)}")
                    return False
            else:
                self.log_test("Community Ideas Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Community Ideas Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_community_ideas_filtering_sorting(self):
        """Test community ideas filtering and sorting"""
        try:
            # Test category filtering
            response1 = self.session.get(f"{self.base_url}/ideas/community?category=Technology")
            
            # Test sorting by validation_score
            response2 = self.session.get(f"{self.base_url}/ideas/community?sort_by=validation_score")
            
            # Test sorting by created_at
            response3 = self.session.get(f"{self.base_url}/ideas/community?sort_by=created_at")
            
            # Test pagination
            response4 = self.session.get(f"{self.base_url}/ideas/community?skip=0&limit=5")
            
            if all(r.status_code == 200 for r in [response1, response2, response3, response4]):
                self.log_test("Community Ideas Filtering Sorting", True, 
                            "Community ideas filtering, sorting, and pagination working")
                return True
            else:
                failed_responses = [i for i, r in enumerate([response1, response2, response3, response4], 1) 
                                  if r.status_code != 200]
                self.log_test("Community Ideas Filtering Sorting", False, 
                            f"Failed responses: {failed_responses}")
                return False
                
        except Exception as e:
            self.log_test("Community Ideas Filtering Sorting", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_submitted_ideas_integration(self):
        """Test that dashboard includes submitted ideas count"""
        try:
            if not self.auth_token:
                self.log_test("Dashboard Submitted Ideas Integration", False, "No auth token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(f"{self.base_url}/user/dashboard", headers=headers)
            
            if response.status_code == 200:
                dashboard_data = response.json()
                
                # Check if submitted ideas are included in user stats
                user_stats = dashboard_data.get("user_stats", {})
                if "total_submitted_ideas" in user_stats:
                    submitted_count = user_stats["total_submitted_ideas"]
                    
                    # Check if submitted ideas appear in recent activity
                    recent_activity = dashboard_data.get("recent_activity", {})
                    if "submitted_ideas" in recent_activity:
                        self.log_test("Dashboard Submitted Ideas Integration", True, 
                                    f"Dashboard includes {submitted_count} submitted ideas in stats and recent activity")
                        return True
                    else:
                        self.log_test("Dashboard Submitted Ideas Integration", False, 
                                    "Submitted ideas missing from recent activity")
                        return False
                else:
                    self.log_test("Dashboard Submitted Ideas Integration", False, 
                                "total_submitted_ideas missing from user stats")
                    return False
            else:
                self.log_test("Dashboard Submitted Ideas Integration", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Submitted Ideas Integration", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests in priority order"""
        print("=" * 60)
        print("BACKEND API TESTING FOR IDEAHERO.COM")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print()
        
        # Test in priority order as specified
        tests = [
            ("Basic Connectivity", self.test_basic_connectivity),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Token Validation", self.test_authentication_token_validation),
            ("Profile Updates", self.test_profile_updates),
            ("Enhanced Ideas API", self.test_enhanced_ideas_api),
            ("Ideas Filtering & Sorting", self.test_ideas_filtering_sorting),
            ("Single Idea Details", self.test_single_idea_details),
            ("Idea Voting System", self.test_idea_voting_system),
            ("Comment System", self.test_comment_system),
            ("Authentication Requirements", self.test_authentication_requirements),
            ("Input Validation", self.test_input_validation),
            ("User Dashboard Authentication", self.test_user_dashboard_authentication),
            ("User Dashboard Data", self.test_user_dashboard_data),
            ("User Analytics Authentication", self.test_user_analytics_authentication),
            ("User Analytics Data", self.test_user_analytics_data),
            ("Dashboard Analytics Integration", self.test_dashboard_analytics_integration),
            # Idea Submission System Tests
            ("Idea Submission Authentication", self.test_idea_submission_authentication),
            ("Idea Submission Valid Data", self.test_idea_submission_valid_data),
            ("Idea Submission Reputation Increase", self.test_idea_submission_reputation_increase),
            ("User Submitted Ideas Authentication", self.test_user_submitted_ideas_authentication),
            ("User Submitted Ideas Data", self.test_user_submitted_ideas_data),
            ("Submitted Idea Details Authentication", self.test_submitted_idea_details_authentication),
            ("Submitted Idea Details Data", self.test_submitted_idea_details_data),
            ("Submitted Idea Details 404", self.test_submitted_idea_details_404),
            ("Update Submitted Idea Authentication", self.test_update_submitted_idea_authentication),
            ("Update Submitted Idea Valid", self.test_update_submitted_idea_valid),
            ("Delete Submitted Idea Authentication", self.test_delete_submitted_idea_authentication),
            ("Delete Submitted Idea Valid", self.test_delete_submitted_idea_valid),
            ("Community Ideas Endpoint", self.test_community_ideas_endpoint),
            ("Community Ideas Filtering Sorting", self.test_community_ideas_filtering_sorting),
            ("Dashboard Submitted Ideas Integration", self.test_dashboard_submitted_ideas_integration)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n--- Testing {test_name} ---")
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ FAIL: {test_name} - Exception: {str(e)}")
                failed += 1
            
            time.sleep(0.5)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print("BACKEND TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {passed + failed}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("\n🎉 ALL BACKEND TESTS PASSED!")
        else:
            print(f"\n⚠️  {failed} TESTS FAILED - See details above")
        
        return failed == 0

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)