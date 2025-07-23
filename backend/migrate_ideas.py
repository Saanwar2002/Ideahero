#!/usr/bin/env python3
"""
Data migration script to enhance existing ideas with validation features
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid
import sys

# Add parent directory to path to import from server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def migrate_ideas():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Starting idea migration...")
    
    # Sample enhanced ideas to seed the database
    sample_ideas = [
        {
            "id": str(uuid.uuid4()),
            "title": "AI-Powered Code Review Assistant for Development Teams",
            "description": "An intelligent code review tool that uses machine learning to automatically identify bugs, security vulnerabilities, performance issues, and code quality problems before deployment. The system learns from your team's coding patterns and provides personalized suggestions to improve code quality and reduce review time.",
            "tags": [
                {"label": "High Demand", "type": "advantage", "icon": "🔥"},
                {"label": "Tech Ready", "type": "ready", "icon": "✅"},
                {"label": "Growing Market", "type": "timing", "icon": "📈"}
            ],
            "category": "Technology",
            "source": "HackerNews",
            "source_url": "https://news.ycombinator.com/item?id=example1",
            "created_at": datetime.utcnow(),
            "votes": [],
            "comments": [],
            "implementation_guide": {
                "steps": [
                    "Market research and competitor analysis",
                    "Define MVP features and technical requirements",
                    "Build AI model for code analysis",
                    "Develop integration with popular IDEs",
                    "Create user dashboard and reporting",
                    "Beta testing with development teams",
                    "Launch and iterate based on feedback"
                ],
                "estimated_time": "6-12 months",
                "estimated_budget": "$50,000 - $150,000",
                "required_skills": ["Machine Learning", "Software Development", "DevOps"],
                "difficulty": "Advanced"
            },
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Transparent HVAC Pricing Platform - End Quote Anxiety For Homeowners",
            "description": "Homeowners dread HVAC repairs because of unpredictable pricing and questionable quotes. TruPrice HVAC transforms this experience with transparent, real-time pricing that eliminates the uncertainty and mistrust. The platform shows exact costs for parts, labor, and service fees before you commit to anything.",
            "tags": [
                {"label": "Perfect Timing", "type": "timing", "icon": "⏰"},
                {"label": "Unfair Advantage", "type": "advantage", "icon": "⚡"},
                {"label": "Product Ready", "type": "ready", "icon": "✅"}
            ],
            "category": "Business",
            "source": "HackerNews",
            "source_url": "https://news.ycombinator.com/item?id=example2",
            "created_at": datetime.utcnow(),
            "votes": [],
            "comments": [],
            "implementation_guide": {
                "steps": [
                    "Research HVAC industry pricing standards",
                    "Build database of parts and labor costs",
                    "Create contractor network and onboarding",
                    "Develop customer-facing pricing calculator",
                    "Build booking and scheduling system",
                    "Launch in target metropolitan area",
                    "Scale to additional markets"
                ],
                "estimated_time": "8-18 months",
                "estimated_budget": "$100,000 - $300,000",
                "required_skills": ["Business Development", "Web Development", "Sales"],
                "difficulty": "Intermediate"
            },
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Remote Team Wellness & Productivity Tracker",
            "description": "A comprehensive platform that helps remote teams track wellness metrics, productivity patterns, and team engagement. Uses AI to provide personalized recommendations for better work-life balance and team collaboration. Includes features for mood tracking, break reminders, and team building activities.",
            "tags": [
                {"label": "Remote Work Trend", "type": "timing", "icon": "🏠"},
                {"label": "Mental Health Focus", "type": "advantage", "icon": "🧠"},
                {"label": "MVP Ready", "type": "ready", "icon": "🚀"}
            ],
            "category": "Healthcare",
            "source": "GitHub",
            "source_url": "https://github.com/example/remote-wellness",
            "created_at": datetime.utcnow(),
            "votes": [],
            "comments": [],
            "implementation_guide": {
                "steps": [
                    "Survey remote workers about wellness needs",
                    "Design user experience and wellness metrics",
                    "Build core tracking and analytics features",
                    "Integrate with popular productivity tools",
                    "Develop AI recommendation engine",
                    "Beta test with remote teams",
                    "Launch freemium model"
                ],
                "estimated_time": "4-8 months",
                "estimated_budget": "$30,000 - $80,000",
                "required_skills": ["UX Design", "Data Analytics", "Psychology"],
                "difficulty": "Beginner"
            },
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Sustainable Supply Chain Transparency Platform",
            "description": "A blockchain-based platform that provides complete transparency in supply chains, allowing consumers to trace products from source to shelf. Features sustainability scoring, carbon footprint tracking, and ethical sourcing verification. Helps brands build trust and consumers make informed choices.",
            "tags": [
                {"label": "Sustainability Trend", "type": "timing", "icon": "🌱"},
                {"label": "Blockchain Ready", "type": "ready", "icon": "⛓️"},
                {"label": "B2B Opportunity", "type": "advantage", "icon": "💼"}
            ],
            "category": "Sustainability",
            "source": "GitHub",
            "source_url": "https://github.com/example/supply-transparency",
            "created_at": datetime.utcnow(),
            "votes": [],
            "comments": [],
            "implementation_guide": {
                "steps": [
                    "Research supply chain pain points",
                    "Choose blockchain platform and architecture",
                    "Build product tracking and verification system",
                    "Create brand dashboard and consumer app",
                    "Pilot with sustainable brands",
                    "Scale platform and onboard retailers",
                    "Expand to international markets"
                ],
                "estimated_time": "12-24 months",
                "estimated_budget": "$200,000 - $500,000",
                "required_skills": ["Blockchain", "Supply Chain", "Business Development"],
                "difficulty": "Advanced"
            },
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Local Skills Exchange & Learning Marketplace",
            "description": "A community-driven platform where people can exchange skills, teach each other, and learn new abilities through local meetups and online sessions. Features skill matching, progress tracking, and community building tools. Focuses on practical skills like cooking, DIY, technology, and creative arts.",
            "tags": [
                {"label": "Community Building", "type": "advantage", "icon": "👥"},
                {"label": "Local Focus", "type": "timing", "icon": "📍"},
                {"label": "Low Startup Cost", "type": "ready", "icon": "💰"}
            ],
            "category": "Education",
            "source": "Community",
            "source_url": "https://example.com/community-discussion",
            "created_at": datetime.utcnow(),
            "votes": [],
            "comments": [],
            "implementation_guide": {
                "steps": [
                    "Identify target community and core skills",
                    "Build MVP with basic matching features",
                    "Create event planning and scheduling tools",
                    "Develop skill tracking and reputation system",
                    "Launch in local community",
                    "Build referral and growth features",
                    "Expand to neighboring communities"
                ],
                "estimated_time": "3-6 months",
                "estimated_budget": "$10,000 - $30,000",
                "required_skills": ["Community Management", "Web Development", "Marketing"],
                "difficulty": "Beginner"
            },
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0
        }
    ]
    
    # Insert sample ideas
    for idea in sample_ideas:
        existing = await db.ideas.find_one({"title": idea["title"]})
        if not existing:
            await db.ideas.insert_one(idea)
            print(f"Added idea: {idea['title']}")
        else:
            print(f"Idea already exists: {idea['title']}")
    
    print(f"Migration complete! Added {len(sample_ideas)} enhanced ideas.")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_ideas())