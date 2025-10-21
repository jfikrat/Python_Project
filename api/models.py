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


class PlanRequest(BaseModel):
    """Request for generating shot plans."""

    product: str = Field(..., description="Product name")
    idea_id: str = Field(..., description="Selected idea ID (e.g., I1)")
    count: int = Field(..., ge=1, le=12, description="Number of shots to generate")


class CameraSettings(BaseModel):
    """Camera settings for a shot."""

    angle: str = Field(..., description="Camera angle (e.g., 45 derece, top-down)")
    lens: str = Field(..., description="Lens focal length (e.g., 50mm)")
    aperture: str = Field(..., description="Aperture setting (e.g., f/2.8)")


class ShotPlan(BaseModel):
    """Detailed plan for a single shot."""

    index: int = Field(..., ge=1, description="Shot number")
    title: str = Field(..., description="Short descriptive title")
    camera: CameraSettings = Field(..., description="Camera configuration")
    lighting: str = Field(..., description="Lighting setup description")
    background: str = Field(..., description="Background/environment details")
    props: str = Field(..., description="Props and accessories (or 'none')")
    composition: str = Field(..., description="Composition guidelines")
    instructions: str = Field(..., description="Step-by-step shooting instructions")
    gen_prompt: str | None = Field(
        None, description="Optional image generation prompt"
    )


class PlanResponse(BaseModel):
    """Response from plan generation endpoint."""

    shots: list[ShotPlan] = Field(..., description="Generated shot plans")
