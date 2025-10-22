import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from agents import ProductPhotoAgent
from services import OpenAIService, ImageService, SessionService
from api.models import (
    ProductDetectionResponse,
    IdeaSuggestion,
    PlanRequest,
    PlanResponse,
)
from config.style_templates import get_all_styles

logger = logging.getLogger(__name__)

# Initialize services
openai_service = OpenAIService()
image_service = ImageService()
session_service = SessionService()
agent = ProductPhotoAgent(openai_service)

# Create router
router = APIRouter(prefix="/api", tags=["Product Photo Agent"])


@router.post("/detect", response_model=ProductDetectionResponse)
async def detect_product(
    file: UploadFile = File(..., description="Product image file"),
    style: str = None,
    model_preference: str = None,
    ai_model: str = None
):
    """
    Step 1 & 2: Detect product and generate shoot ideas.

    Upload a product image to:
    1. Identify the product (name, category, attributes)
    2. Receive 5 creative shoot idea suggestions (optionally with style and model preferences)

    Args:
        file: Product image file
        style: Optional style preference (minimal, luxury, lifestyle, vintage, bold, industrial, decorative)
        model_preference: Optional model preference ('with_model' or 'without_model')
        ai_model: Optional AI model to use (gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o-mini)

    Returns:
        ProductDetectionResponse with product details and ideas
    """
    try:
        logger.info(f"Processing detection request for file: {file.filename}")

        # Read file content
        file_content = await file.read()

        # Validate image
        is_valid, error_msg = image_service.validate_image(file_content, file.filename)
        if not is_valid:
            logger.warning(f"Invalid image: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        # Optimize image for API (always converts to JPEG)
        optimized_content = image_service.optimize_for_api(file_content)

        # Convert to data URL with correct MIME type (JPEG after optimization)
        data_url = image_service.to_base64_data_url(optimized_content, mime_type="image/jpeg")

        # Step 1: Detect product (async)
        log_msg = "Detecting product..."
        if ai_model:
            log_msg += f" using {ai_model}"
        logger.info(log_msg)
        product_data = await agent.detect_product(data_url, model=ai_model)

        # Step 2: Generate ideas (async)
        log_msg = f"Generating ideas for: {product_data['product']}"
        if style:
            log_msg += f" with style: {style}"
        if model_preference:
            log_msg += f", model preference: {model_preference}"
        if ai_model:
            log_msg += f", using {ai_model}"
        logger.info(log_msg)

        ideas_data = await agent.suggest_ideas(
            product=product_data["product"],
            category=product_data["category"],
            attributes=product_data.get("attributes", []),
            style=style,
            model_preference=model_preference,
            model=ai_model
        )

        # Store idea details in session for later retrieval
        session_data = {
            "product": product_data["product"],
            "category": product_data["category"],
            "attributes": product_data.get("attributes", []),
            "ideas": ideas_data.get("ideas", []),
            "model_preference": model_preference,  # Store for shot plan generation
        }
        session_id = session_service.create_session(session_data)
        logger.info(f"Created session {session_id} with {len(ideas_data.get('ideas', []))} ideas")

        # Combine responses
        response = {
            "product": product_data["product"],
            "category": product_data["category"],
            "attributes": product_data.get("attributes", []),
            "confidence": product_data.get("confidence", 0),
            "ideas": ideas_data.get("ideas", []),
            "session_id": session_id,
        }

        logger.info(f"Detection successful: {product_data['product']} ({len(ideas_data.get('ideas', []))} ideas)")
        return ProductDetectionResponse(**response)

    except ValueError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"JSON parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/plan", response_model=PlanResponse)
async def generate_plan(request: PlanRequest):
    """
    Step 3: Generate image generation prompts.

    Provide:
    - product: Product name from /detect response
    - idea_id: Selected idea ID (e.g., "I1")
    - count: Number of prompts to generate (1-12)

    Returns:
        PlanResponse with image generation prompts (DALL-E/Midjourney/SD compatible)
    """
    try:
        logger.info(f"Generating {request.count} prompts for product: {request.product}, idea: {request.idea_id}")

        # Retrieve session data
        session_data = session_service.get_session(request.session_id)
        if session_data is None:
            logger.warning(f"Session not found or expired: {request.session_id}")
            raise HTTPException(status_code=404, detail="Session not found or expired. Please upload the image again.")

        # Find the selected idea from session data
        ideas = session_data.get("ideas", [])
        selected_idea = next((idea for idea in ideas if idea.get("id") == request.idea_id), None)

        if selected_idea is None:
            logger.warning(f"Idea {request.idea_id} not found in session {request.session_id}")
            raise HTTPException(status_code=404, detail=f"Idea {request.idea_id} not found in session")

        logger.info(f"Retrieved idea '{selected_idea.get('title')}' from session")

        # Retrieve model preference from session
        model_preference = session_data.get("model_preference")

        # Generate image generation prompts (async)
        log_msg = f"Generating {request.count} prompts for idea '{selected_idea.get('title')}'"
        if model_preference:
            log_msg += f" with model preference: {model_preference}"
        if request.ai_model:
            log_msg += f" using {request.ai_model}"
        logger.info(log_msg)

        plan_data = await agent.build_shot_plan(
            product=request.product,
            selected_idea=selected_idea,
            count=request.count,
            model_preference=model_preference,
            model=request.ai_model
        )

        logger.info(f"Successfully generated {len(plan_data.get('shots', []))} prompts")
        return PlanResponse(**plan_data)

    except ValueError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"JSON parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/styles")
async def get_styles():
    """
    Get available photo shoot styles.

    Returns:
        List of available styles with names and descriptions
    """
    return {"styles": get_all_styles()}


@router.get("/models")
async def get_models():
    """
    Get available AI models for user selection.

    Returns:
        Dictionary of available models with details
    """
    from config import settings
    return {
        "models": settings.available_models,
        "default": settings.openai_model
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Product Photo Agent API"}
