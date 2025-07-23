#!/usr/bin/env python3
"""
Seed test data for IdeaHero.com to test dashboard and analytics functionality
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
import uuid

ROOT_DIR = Path('backend')
load_dotenv(ROOT_DIR / '.env')

async def seed_test_data():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Create test ideas
    test_ideas = [
        {
            "id": str(uuid.uuid4()),
            "title": "AI-Powered Personal Finance Assistant",
            "description": "A mobile app that uses machine learning to analyze spending patterns and provide personalized financial advice.",
            "category": "FinTech",
            "source": "HackerNews",
            "created_at": datetime.utcnow() - timedelta(days=10),
            "votes": [],
            "comments": [],
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0,
            "tags": [{"name": "AI", "color": "blue"}, {"name": "Finance", "color": "green"}]
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Smart Home Energy Optimization Platform",
            "description": "IoT-based system that automatically optimizes home energy consumption using real-time data and weather forecasts.",
            "category": "Technology",
            "source": "HackerNews", 
            "created_at": datetime.utcnow() - timedelta(days=5),
            "votes": [],
            "comments": [],
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0,
            "tags": [{"name": "IoT", "color": "purple"}, {"name": "Energy", "color": "yellow"}]
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Virtual Reality Fitness Training Platform",
            "description": "Immersive VR fitness experience with AI personal trainers and social workout features.",
            "category": "Health & Fitness",
            "source": "HackerNews",
            "created_at": datetime.utcnow() - timedelta(days=2),
            "votes": [],
            "comments": [],
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0,
            "tags": [{"name": "VR", "color": "red"}, {"name": "Fitness", "color": "orange"}]
        }
    ]
    
    # Insert ideas
    await db.ideas.insert_many(test_ideas)
    print(f"✅ Inserted {len(test_ideas)} test ideas")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_test_data())