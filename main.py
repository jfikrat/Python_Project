import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from api.routes import router
from logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
)

# Add CORS middleware (for web frontend)
# Configure via CORS_ORIGINS in .env.local
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured with origins: {settings.get_cors_origins()}")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Serve the UI homepage."""
    return FileResponse("index.html")


@app.get("/chat")
async def chat():
    """Serve the chat UI."""
    return FileResponse("chat.html")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Product Photo Agent API...")
    logger.info(f"Server will run on http://0.0.0.0:8000")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_config=None  # Use our custom logging config
    )
