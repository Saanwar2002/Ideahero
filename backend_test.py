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
BACKEND_URL = "https://3e206a03-0a5a-40c5-b20b-32fd42b7e8c5.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_id = None
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
            ("Input Validation", self.test_input_validation)
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