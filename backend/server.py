from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from database import connect_to_mongo, close_mongo_connection
from routes import menu, orders, newsletter, admin


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(
    title="Tantawan Restaurant API",
    description="API for Tantawan Asian Restaurant ordering, newsletter system, and admin management",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add route modules
api_router.include_router(menu.router)
api_router.include_router(orders.router)
api_router.include_router(newsletter.router)
api_router.include_router(admin.router)

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Tantawan Restaurant API", "status": "healthy"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Tantawan Restaurant API"}

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

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()