from app.main import app
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with actual origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)