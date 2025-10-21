from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from agents import ProductPhotoAgent
from services import OpenAIService, ImageService
from api.models import (
    ProductDetectionResponse,
    IdeaSuggestion,
    PlanRequest,
    PlanResponse,
)

# Initialize services
openai_service = OpenAIService()
image_service = ImageService()
agent = ProductPhotoAgent(openai_service)

# Create router
router = APIRouter(prefix="/api", tags=["Product Photo Agent"])


@router.post("/detect", response_model=ProductDetectionResponse)
async def detect_product(
    file: UploadFile = File(..., description="Product image file")
):
    """
    Step 1 & 2: Detect product and generate shoot ideas.

    Upload a product image to:
    1. Identify the product (name, category, attributes)
    2. Receive 5 creative shoot idea suggestions

    Returns:
        ProductDetectionResponse with product details and ideas
    """
    try:
        # Read file content
        file_content = await file.read()

        # Validate image
        is_valid, error_msg = image_service.validate_image(file_content, file.filename)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Optimize image for API
        optimized_content = image_service.optimize_for_api(file_content)

        # Convert to data URL
        data_url = image_service.to_base64_data_url(optimized_content, file.filename)

        # Step 1: Detect product
        product_data = agent.detect_product(data_url)

        # Step 2: Generate ideas
        ideas_data = agent.suggest_ideas(
            product=product_data["product"],
            category=product_data["category"],
            attributes=product_data.get("attributes", []),
        )

        # Combine responses
        response = {
            "product": product_data["product"],
            "category": product_data["category"],
            "attributes": product_data.get("attributes", []),
            "confidence": product_data.get("confidence", 0),
            "ideas": ideas_data.get("ideas", []),
        }

        return ProductDetectionResponse(**response)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"JSON parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/plan", response_model=PlanResponse)
async def generate_plan(request: PlanRequest):
    """
    Step 3: Generate detailed shot plans.

    Provide:
    - product: Product name from /detect response
    - idea_id: Selected idea ID (e.g., "I1")
    - count: Number of shots to generate (1-12)

    Returns:
        PlanResponse with detailed shot plans
    """
    try:
        # Create selected_idea structure for the agent
        # In a real app, you'd store the full idea data from step 2
        # For now, we'll pass minimal info and let the agent recreate context
        selected_idea = {
            "id": request.idea_id,
            "title": f"Idea {request.idea_id}",
            # Note: In production, you'd retrieve the full idea from storage/session
        }

        # Generate shot plans
        plan_data = agent.build_shot_plan(
            product=request.product,
            selected_idea=selected_idea,
            count=request.count,
        )

        return PlanResponse(**plan_data)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"JSON parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Product Photo Agent API"}
