from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import hashlib
import jwt
from passlib.context import CryptContext
import re


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    skills: List[str] = []
    interests: List[str] = []
    experience_level: str = "beginner"  # beginner, intermediate, advanced

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    full_name: str
    skills: List[str] = []
    interests: List[str] = []
    experience_level: str = "beginner"
    reputation_score: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    skills: List[str]
    interests: List[str]
    experience_level: str
    reputation_score: int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Idea Models
class IdeaVote(BaseModel):
    user_id: str
    vote_type: str  # upvote, downvote
    feasibility_score: int  # 1-5
    market_potential_score: int  # 1-5
    interest_score: int  # 1-5
    created_at: datetime = Field(default_factory=datetime.utcnow)

class IdeaComment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    likes: int = 0

class EnhancedIdea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    tags: List[Dict[str, Any]] = []
    category: str
    source: str = "HackerNews"
    source_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    votes: List[IdeaVote] = []
    comments: List[IdeaComment] = []
    implementation_guide: Optional[Dict[str, Any]] = None
    validation_score: float = 0.0
    total_votes: int = 0
    avg_feasibility: float = 0.0
    avg_market_potential: float = 0.0
    avg_interest: float = 0.0

class VoteCreate(BaseModel):
    idea_id: str
    vote_type: str
    feasibility_score: int
    market_potential_score: int
    interest_score: int

class CommentCreate(BaseModel):
    idea_id: str
    content: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
