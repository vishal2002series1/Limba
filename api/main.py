from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Define the path to the .env file
DOTENV_FILEPATH = os.path.join('..', '.env')
DEV_ENV = os.path.exists(DOTENV_FILEPATH)

# Load environment variables based on the environment
if DEV_ENV:
    print("DEV ENV")
    print("LOADING ENV VARIABLES...")
    load_dotenv(DOTENV_FILEPATH, override=True)
else:
    print("PROD ENV")

# Import necessary modules
from app.modules import chat, auth

# Initialize FastAPI app
app = FastAPI()

# Include routers for different endpoints
app.include_router(auth.api.router, prefix="/irah/auth", tags=["Auth"])
app.include_router(chat.api.router, prefix="/irah/chat", tags=["Chat"])
app.include_router(chat.api.router1, prefix="/irah/files", tags=["Files"])
app.include_router(chat.api.advisor_copilot, prefix="/irah/advisor_copilot", tags=["Advisor Copilot"])

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return "IRAH API Service is running..."