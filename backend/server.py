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

# Authentication Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise credentials_exception
    return User(**user)

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    return len(password) >= 6

# Helper function to calculate idea scores
def calculate_idea_scores(votes: List[IdeaVote]) -> Dict[str, float]:
    if not votes:
        return {
            "validation_score": 0.0,
            "total_votes": 0,
            "avg_feasibility": 0.0,
            "avg_market_potential": 0.0,
            "avg_interest": 0.0
        }
    
    total_votes = len(votes)
    upvotes = len([v for v in votes if v.vote_type == "upvote"])
    downvotes = len([v for v in votes if v.vote_type == "downvote"])
    
    avg_feasibility = sum(v.feasibility_score for v in votes) / total_votes
    avg_market_potential = sum(v.market_potential_score for v in votes) / total_votes
    avg_interest = sum(v.interest_score for v in votes) / total_votes
    
    # Calculate validation score (weighted average)
    vote_ratio = upvotes / total_votes if total_votes > 0 else 0
    score_average = (avg_feasibility + avg_market_potential + avg_interest) / 3
    validation_score = (vote_ratio * 0.4 + score_average/5 * 0.6) * 100
    
    return {
        "validation_score": round(validation_score, 1),
        "total_votes": total_votes,
        "avg_feasibility": round(avg_feasibility, 1),
        "avg_market_potential": round(avg_market_potential, 1),
        "avg_interest": round(avg_interest, 1)
    }
# Authentication Routes
@api_router.post("/auth/register", response_model=Token)
async def register_user(user_data: UserCreate):
    # Validate email format
    if not validate_email(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate password strength
    if not validate_password(user_data.password):
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        skills=user_data.skills,
        interests=user_data.interests,
        experience_level=user_data.experience_level
    )
    
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    
    await db.users.insert_one(user_dict)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**user.dict())
    )

@api_router.post("/auth/login", response_model=Token)
async def login_user(user_credentials: UserLogin):
    # Find user by email
    user_doc = await db.users.find_one({"email": user_credentials.email})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(user_credentials.password, user_doc.get("hashed_password", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_doc["id"]}, expires_delta=access_token_expires
    )
    
    user = User(**user_doc)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**user.dict())
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

@api_router.put("/auth/profile", response_model=UserResponse)
async def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user)
):
    # Update allowed fields
    allowed_fields = ["full_name", "skills", "interests", "experience_level"]
    update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
    
    if update_data:
        await db.users.update_one(
            {"id": current_user.id},
            {"$set": update_data}
        )
    
    # Get updated user
    updated_user = await db.users.find_one({"id": current_user.id})
    return UserResponse(**User(**updated_user).dict())

# Idea Routes
@api_router.post("/ideas/{idea_id}/vote")
async def vote_on_idea(
    idea_id: str,
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user)
):
    # Validate scores
    for score in [vote_data.feasibility_score, vote_data.market_potential_score, vote_data.interest_score]:
        if score < 1 or score > 5:
            raise HTTPException(status_code=400, detail="Scores must be between 1 and 5")
    
    # Check if idea exists
    idea = await db.ideas.find_one({"id": idea_id})
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Create vote object
    vote = IdeaVote(
        user_id=current_user.id,
        vote_type=vote_data.vote_type,
        feasibility_score=vote_data.feasibility_score,
        market_potential_score=vote_data.market_potential_score,
        interest_score=vote_data.interest_score
    )
    
    # Remove existing vote from this user if exists
    await db.ideas.update_one(
        {"id": idea_id},
        {"$pull": {"votes": {"user_id": current_user.id}}}
    )
    
    # Add new vote
    await db.ideas.update_one(
        {"id": idea_id},
        {"$push": {"votes": vote.dict()}}
    )
    
    # Update user reputation
    reputation_change = 2 if vote_data.vote_type == "upvote" else 1
    await db.users.update_one(
        {"id": current_user.id},
        {"$inc": {"reputation_score": reputation_change}}
    )
    
    # Recalculate idea scores
    updated_idea = await db.ideas.find_one({"id": idea_id})
    scores = calculate_idea_scores([IdeaVote(**v) for v in updated_idea.get("votes", [])])
    
    await db.ideas.update_one(
        {"id": idea_id},
        {"$set": scores}
    )
    
    return {"message": "Vote recorded successfully", "scores": scores}

@api_router.post("/ideas/{idea_id}/comment")
async def comment_on_idea(
    idea_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user)
):
    # Check if idea exists
    idea = await db.ideas.find_one({"id": idea_id})
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Create comment
    comment = IdeaComment(
        user_id=current_user.id,
        user_name=current_user.full_name,
        content=comment_data.content.strip()
    )
    
    if len(comment.content) < 10:
        raise HTTPException(status_code=400, detail="Comment must be at least 10 characters long")
    
    # Add comment to idea
    await db.ideas.update_one(
        {"id": idea_id},
        {"$push": {"comments": comment.dict()}}
    )
    
    # Update user reputation
    await db.users.update_one(
        {"id": current_user.id},
        {"$inc": {"reputation_score": 1}}
    )
    
    return {"message": "Comment added successfully", "comment": comment.dict()}

@api_router.get("/ideas", response_model=List[EnhancedIdea])
async def get_all_ideas(
    category: Optional[str] = None,
    sort_by: str = "validation_score",  # validation_score, created_at, total_votes
    limit: int = 20,
    skip: int = 0
):
    query = {}
    if category and category != "All":
        query["category"] = category
    
    # Sort options
    sort_field = "validation_score"
    sort_order = -1  # Descending
    
    if sort_by == "created_at":
        sort_field = "created_at" 
    elif sort_by == "total_votes":
        sort_field = "total_votes"
    
    ideas = await db.ideas.find(query).sort(sort_field, sort_order).skip(skip).limit(limit).to_list(limit)
    
    return [EnhancedIdea(**idea) for idea in ideas]

@api_router.get("/ideas/{idea_id}", response_model=EnhancedIdea)
async def get_idea_details(idea_id: str):
    idea = await db.ideas.find_one({"id": idea_id})
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    return EnhancedIdea(**idea)

# User Dashboard & Analytics Endpoints
@api_router.get("/user/dashboard")
async def get_user_dashboard(current_user: User = Depends(get_current_user)):
    """Get comprehensive user dashboard data"""
    user_id = current_user.id
    
    # Get user's voting activity
    user_votes = await db.ideas.find({"votes.user_id": user_id}).to_list(1000)
    total_votes = sum(len([vote for vote in idea["votes"] if vote["user_id"] == user_id]) for idea in user_votes)
    
    # Get user's comments
    user_comments = await db.ideas.find({"comments.user_id": user_id}).to_list(1000)
    total_comments = sum(len([comment for comment in idea["comments"] if comment["user_id"] == user_id]) for idea in user_comments)
    
    # Get ideas the user has voted on recently
    recent_voted_ideas = []
    for idea in user_votes[-5:]:  # Last 5 ideas voted on
        user_vote = next((vote for vote in idea["votes"] if vote["user_id"] == user_id), None)
        if user_vote:
            recent_voted_ideas.append({
                "idea_id": idea["id"],
                "idea_title": idea["title"],
                "vote_type": user_vote["vote_type"],
                "voted_at": user_vote["created_at"]
            })
    
    # Get user's commented ideas
    recent_commented_ideas = []
    for idea in user_comments[-5:]:  # Last 5 ideas commented on
        user_comment = next((comment for comment in idea["comments"] if comment["user_id"] == user_id), None)
        if user_comment:
            recent_commented_ideas.append({
                "idea_id": idea["id"],
                "idea_title": idea["title"],
                "comment_preview": user_comment["content"][:100] + "..." if len(user_comment["content"]) > 100 else user_comment["content"],
                "commented_at": user_comment["created_at"]
            })
    
    # Calculate engagement metrics
    upvotes_given = sum(len([vote for vote in idea["votes"] if vote["user_id"] == user_id and vote["vote_type"] == "upvote"]) for idea in user_votes)
    downvotes_given = sum(len([vote for vote in idea["votes"] if vote["user_id"] == user_id and vote["vote_type"] == "downvote"]) for idea in user_votes)
    
    # Get user's favorite categories (based on voting patterns)
    category_votes = {}
    for idea in user_votes:
        category = idea.get("category", "Other")
        category_votes[category] = category_votes.get(category, 0) + 1
    
    favorite_categories = sorted(category_votes.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "user_stats": {
            "total_votes": total_votes,
            "total_comments": total_comments,
            "upvotes_given": upvotes_given,
            "downvotes_given": downvotes_given,
            "reputation_score": current_user.reputation_score,
            "member_since": current_user.created_at,
            "favorite_categories": [{"category": cat, "count": count} for cat, count in favorite_categories]
        },
        "recent_activity": {
            "voted_ideas": recent_voted_ideas,
            "commented_ideas": recent_commented_ideas
        },
        "engagement_summary": {
            "total_interactions": total_votes + total_comments,
            "vote_ratio": round(upvotes_given / (upvotes_given + downvotes_given) * 100, 1) if (upvotes_given + downvotes_given) > 0 else 0,
            "active_days": 0  # TODO: Calculate based on activity dates
        }
    }

@api_router.get("/user/analytics")
async def get_user_analytics(current_user: User = Depends(get_current_user)):
    """Get user analytics data for charts and graphs"""
    user_id = current_user.id
    
    # Get all ideas the user has interacted with
    user_ideas = await db.ideas.find({
        "$or": [
            {"votes.user_id": user_id},
            {"comments.user_id": user_id}
        ]
    }).to_list(1000)
    
    # Prepare data for charts
    monthly_activity = {}
    category_distribution = {}
    score_distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    
    for idea in user_ideas:
        # Process votes
        user_votes = [vote for vote in idea["votes"] if vote["user_id"] == user_id]
        for vote in user_votes:
            vote_date = vote["created_at"]
            month_key = f"{vote_date.year}-{vote_date.month:02d}"
            
            if month_key not in monthly_activity:
                monthly_activity[month_key] = {"votes": 0, "comments": 0}
            monthly_activity[month_key]["votes"] += 1
            
            # Track category distribution
            category = idea.get("category", "Other")
            category_distribution[category] = category_distribution.get(category, 0) + 1
            
            # Track score distribution
            avg_score = round((vote["feasibility_score"] + vote["market_potential_score"] + vote["interest_score"]) / 3)
            score_distribution[str(avg_score)] += 1
        
        # Process comments
        user_comments = [comment for comment in idea["comments"] if comment["user_id"] == user_id]
        for comment in user_comments:
            comment_date = comment["created_at"]
            month_key = f"{comment_date.year}-{comment_date.month:02d}"
            
            if month_key not in monthly_activity:
                monthly_activity[month_key] = {"votes": 0, "comments": 0}
            monthly_activity[month_key]["comments"] += 1
    
    # Convert to chart-friendly format
    activity_timeline = []
    for month, activity in sorted(monthly_activity.items()):
        activity_timeline.append({
            "month": month,
            "votes": activity["votes"],
            "comments": activity["comments"],
            "total": activity["votes"] + activity["comments"]
        })
    
    return {
        "activity_timeline": activity_timeline,
        "category_distribution": [{"category": cat, "count": count} for cat, count in category_distribution.items()],
        "score_distribution": [{"score": score, "count": count} for score, count in score_distribution.items()],
        "total_interactions": sum(activity["votes"] + activity["comments"] for activity in monthly_activity.values())
    }

# Add your existing routes
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
