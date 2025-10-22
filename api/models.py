from pydantic import BaseModel, Field


class IdeaSuggestion(BaseModel):
    """A single creative shoot idea."""

    id: str = Field(..., description="Unique identifier (e.g., I1, I2)")
    title: str = Field(..., description="Short title for the idea")
    summary: str = Field(..., description="Brief description of the concept")
    why_it_works: str = Field(..., description="Commercial justification")
    shot_keywords: list[str] = Field(
        ..., description="Visual keywords (e.g., flatlay, soft light)"
    )


class ProductDetectionResponse(BaseModel):
    """Response from product detection endpoint."""

    product: str = Field(..., description="Detected product name")
    category: str = Field(..., description="Product category")
    attributes: list[str] = Field(..., description="Product attributes")
    confidence: int = Field(..., ge=0, le=100, description="Detection confidence (0-100)")
    ideas: list[IdeaSuggestion] = Field(..., description="Suggested shoot ideas")
    session_id: str = Field(..., description="Session ID for storing idea details")


class PlanRequest(BaseModel):
    """Request for generating shot plans."""

    product: str = Field(..., description="Product name")
    idea_id: str = Field(..., description="Selected idea ID (e.g., I1)")
    count: int = Field(..., ge=1, le=12, description="Number of shots to generate")
    session_id: str = Field(..., description="Session ID to retrieve idea details")
    ai_model: str | None = Field(None, description="Optional AI model to use")


class ShotPlan(BaseModel):
    """Image generation prompt with metadata."""

    index: int = Field(..., ge=1, description="Shot number")
    title: str = Field(..., description="Short descriptive title")
    style_description: str = Field(..., description="Style and aesthetic description")
    gen_prompt: str = Field(..., description="Image generation prompt for DALL-E/Midjourney/SD")


class PlanResponse(BaseModel):
    """Response from plan generation endpoint."""

    shots: list[ShotPlan] = Field(..., description="Generated shot plans")
