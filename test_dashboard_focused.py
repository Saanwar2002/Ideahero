#!/usr/bin/env python3
"""
Focused test for User Dashboard and Analytics endpoints with test data
"""

import requests
import json
import time
from datetime import datetime

BACKEND_URL = "https://d3f49592-8bfd-4c9e-805c-9412e4dd74fd.preview.emergentagent.com/api"

def test_dashboard_with_activity():
    """Test dashboard and analytics with actual user activity"""
    session = requests.Session()
    
    # Register a test user
    timestamp = int(time.time())
    user_data = {
        "email": f"dashboard.tester{timestamp}@ideahero.com",
        "password": "TestDashboard123!",
        "full_name": "Dashboard Tester",
        "skills": ["Product Management", "Data Analysis"],
        "interests": ["FinTech", "Technology"],
        "experience_level": "intermediate"
    }
    
    print("🔄 Registering test user...")
    reg_response = session.post(f"{BACKEND_URL}/auth/register", json=user_data)
    if reg_response.status_code != 200:
        print(f"❌ Registration failed: {reg_response.status_code}")
        return False
    
    auth_token = reg_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Get available ideas
    print("🔄 Getting available ideas...")
    ideas_response = session.get(f"{BACKEND_URL}/ideas")
    if ideas_response.status_code != 200:
        print(f"❌ Failed to get ideas: {ideas_response.status_code}")
        return False
    
    ideas = ideas_response.json()
    if len(ideas) == 0:
        print("❌ No ideas available for testing")
        return False
    
    print(f"✅ Found {len(ideas)} ideas for testing")
    
    # Vote on some ideas
    print("🔄 Adding votes to create activity...")
    for i, idea in enumerate(ideas[:2]):  # Vote on first 2 ideas
        vote_data = {
            "idea_id": idea["id"],
            "vote_type": "upvote" if i == 0 else "downvote",
            "feasibility_score": 4 + i,
            "market_potential_score": 5 - i,
            "interest_score": 4
        }
        
        vote_response = session.post(f"{BACKEND_URL}/ideas/{idea['id']}/vote", 
                                   json=vote_data, headers=headers)
        if vote_response.status_code == 200:
            print(f"✅ Voted on idea: {idea['title'][:50]}...")
        else:
            print(f"❌ Vote failed: {vote_response.status_code}")
    
    # Add comments
    print("🔄 Adding comments to create activity...")
    for i, idea in enumerate(ideas[:2]):  # Comment on first 2 ideas
        comment_data = {
            "idea_id": idea["id"],
            "content": f"This is a great idea! I particularly like the {idea['category']} approach. The market potential seems very promising and the implementation looks feasible."
        }
        
        comment_response = session.post(f"{BACKEND_URL}/ideas/{idea['id']}/comment", 
                                      json=comment_data, headers=headers)
        if comment_response.status_code == 200:
            print(f"✅ Commented on idea: {idea['title'][:50]}...")
        else:
            print(f"❌ Comment failed: {comment_response.status_code}")
    
    # Test Dashboard Endpoint
    print("\n🔄 Testing User Dashboard endpoint...")
    dashboard_response = session.get(f"{BACKEND_URL}/user/dashboard", headers=headers)
    
    if dashboard_response.status_code == 200:
        dashboard_data = dashboard_response.json()
        
        print("✅ Dashboard endpoint working!")
        print(f"   Total votes: {dashboard_data['user_stats']['total_votes']}")
        print(f"   Total comments: {dashboard_data['user_stats']['total_comments']}")
        print(f"   Reputation score: {dashboard_data['user_stats']['reputation_score']}")
        print(f"   Upvotes given: {dashboard_data['user_stats']['upvotes_given']}")
        print(f"   Downvotes given: {dashboard_data['user_stats']['downvotes_given']}")
        print(f"   Recent voted ideas: {len(dashboard_data['recent_activity']['voted_ideas'])}")
        print(f"   Recent commented ideas: {len(dashboard_data['recent_activity']['commented_ideas'])}")
        print(f"   Favorite categories: {dashboard_data['user_stats']['favorite_categories']}")
        print(f"   Total interactions: {dashboard_data['engagement_summary']['total_interactions']}")
        print(f"   Vote ratio: {dashboard_data['engagement_summary']['vote_ratio']}%")
        
        # Verify we have activity data
        if (dashboard_data['user_stats']['total_votes'] > 0 and 
            dashboard_data['user_stats']['total_comments'] > 0 and
            dashboard_data['user_stats']['reputation_score'] > 0):
            print("✅ Dashboard shows accurate activity data!")
        else:
            print("❌ Dashboard not showing expected activity data")
            return False
    else:
        print(f"❌ Dashboard failed: {dashboard_response.status_code}")
        return False
    
    # Test Analytics Endpoint
    print("\n🔄 Testing User Analytics endpoint...")
    analytics_response = session.get(f"{BACKEND_URL}/user/analytics", headers=headers)
    
    if analytics_response.status_code == 200:
        analytics_data = analytics_response.json()
        
        print("✅ Analytics endpoint working!")
        print(f"   Activity timeline entries: {len(analytics_data['activity_timeline'])}")
        print(f"   Category distribution: {len(analytics_data['category_distribution'])}")
        print(f"   Score distribution: {len(analytics_data['score_distribution'])}")
        print(f"   Total interactions: {analytics_data['total_interactions']}")
        
        # Show some sample data
        if analytics_data['category_distribution']:
            print(f"   Categories: {[cat['category'] for cat in analytics_data['category_distribution']]}")
        
        if analytics_data['activity_timeline']:
            print(f"   Timeline sample: {analytics_data['activity_timeline'][0]}")
        
        # Verify data consistency
        if analytics_data['total_interactions'] == dashboard_data['engagement_summary']['total_interactions']:
            print("✅ Analytics data consistent with dashboard!")
        else:
            print("❌ Analytics data inconsistent with dashboard")
            return False
    else:
        print(f"❌ Analytics failed: {analytics_response.status_code}")
        return False
    
    print("\n🎉 ALL DASHBOARD AND ANALYTICS TESTS PASSED!")
    return True

if __name__ == "__main__":
    success = test_dashboard_with_activity()
    exit(0 if success else 1)