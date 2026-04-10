from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, trees, members
from app.core.config import settings

app = FastAPI(title="轻量级族谱系统 (Lightweight Family Tree)")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(trees.router, prefix="/api/v1/trees", tags=["trees"])
app.include_router(members.router, prefix="/api/v1/members", tags=["members"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Lightweight Family Tree API!"}