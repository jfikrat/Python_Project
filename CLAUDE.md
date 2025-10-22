# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered FastAPI service for product photo shoot planning using OpenAI's GPT-4o-mini Vision. Implements a 3-step agentic workflow: product detection from images, creative shoot idea generation, and detailed shot plan creation.

## Development Setup

### Installation
```bash
pip install -r requirements.txt
```

### Environment Configuration
Create `.env.local` (not `.env`) with required variables:
```
OPENAI_API_KEY=sk-proj-...
```

Optional overrides in `.env.local`:
- `OPENAI_MODEL` (default: `gpt-4o-mini`)
- `OPENAI_TEMPERATURE` (default: `0.4`)
- `OPENAI_MAX_TOKENS` (default: `4000`)

Settings are loaded via `pydantic-settings` in [config/settings.py](config/settings.py).

### Running the Server

**Production mode:**
```bash
python main.py
```

**Development mode with auto-reload:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at `http://localhost:8000`
Interactive API docs at `http://localhost:8000/docs`

## Architecture

### Agentic Workflow Pattern

The core workflow in [agents/photo_agent.py](agents/photo_agent.py) implements three sequential steps:

1. **detect_product()**: Uses GPT-4o-mini Vision to identify product name, category, attributes, and confidence from an uploaded image
2. **suggest_ideas()**: Generates 5 creative shoot concepts based on product characteristics
3. **build_shot_plan()**: Creates image generation prompts (for DALL-E/Midjourney/Stable Diffusion) with title and style descriptions

Each step uses structured JSON prompts and responses. The agent is stateless and receives an `OpenAIService` instance via dependency injection.

### Service Layer

**OpenAIService** ([services/openai_service.py](services/openai_service.py)):
- Wraps OpenAI API client with configured defaults
- `chat_completion()`: Sends messages, returns raw text response
- `extract_json()`: Robust JSON extraction that handles code fences, extra text, and finds JSON boundaries

**ImageService** ([services/image_service.py](services/image_service.py)):
- `validate_image()`: Checks file size, extension, and image integrity
- `optimize_for_api()`: Resizes images to max 2048px dimension, converts to JPEG @85% quality
- `to_base64_data_url()`: Converts image bytes to base64 data URLs for OpenAI Vision API

### API Layer

**Routes** ([api/routes.py](api/routes.py)):
- Services are instantiated at **module level** (not per-request), making them singletons
- POST `/api/detect`: Combines steps 1 & 2 (detect + ideas)
- POST `/api/plan`: Executes step 3 (shot plans)
- GET `/api/health`: Health check

**Models** ([api/models.py](api/models.py)):
- Pydantic models for request/response validation
- Key models: `ProductDetectionResponse`, `PlanRequest`, `PlanResponse`, `ShotPlan`
- `ShotPlan` contains: `index`, `title`, `style_description`, `gen_prompt` (image generation prompt)

### Design Patterns

**Stateless Architecture**: No session storage or state persistence. The `/plan` endpoint requires the user to pass back product details from `/detect` response. In production, this limitation should be addressed with session storage or full idea data in requests.

**JSON Extraction**: LLMs sometimes wrap JSON in markdown code fences or add extra text. `OpenAIService.extract_json()` handles this by finding `{` and `}` boundaries.

**Image Optimization**: Always optimize images before sending to OpenAI API to reduce costs and latency.

**Turkish Prompts**: All user-facing prompts are in Turkish for the Turkish e-commerce photography domain.

## Common Development Tasks

### Testing API Endpoints

**Upload image and detect product:**
```bash
curl -X POST "http://localhost:8000/api/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/product.jpg"
```

**Generate shot plans:**
```bash
curl -X POST "http://localhost:8000/api/plan" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "product": "Nike Air Max 90",
    "idea_id": "I1",
    "count": 5
  }'
```

### Modifying Prompts

Agent prompts are embedded in [agents/photo_agent.py](agents/photo_agent.py) methods:
- `detect_product()`: Product detection via Vision API (Turkish prompts)
- `suggest_ideas()`: Creative shoot concept generation (Turkish prompts)
- `build_shot_plan()`: Image generation prompt engineering (Turkish user text, English output prompts)

The third step generates **English prompts** suitable for DALL-E, Midjourney, or Stable Diffusion. Each prompt includes title and style description metadata.

When modifying prompts, ensure JSON schema documentation matches Pydantic models in [api/models.py](api/models.py).

### Adding New Endpoints

1. Define Pydantic request/response models in [api/models.py](api/models.py)
2. Add endpoint handler in [api/routes.py](api/routes.py)
3. Use existing service instances (`openai_service`, `image_service`, `agent`)
4. Follow error handling pattern: `ValueError` for JSON parsing (422), generic exceptions for processing errors (500)

### Configuration Changes

Edit [config/settings.py](config/settings.py) to add new settings:
- Add field to `Settings` class with type hints
- Set default value or make required
- Override in `.env.local` using uppercase names (e.g., `NEW_SETTING=value`)

## Key Implementation Details

### Vision API Data URLs

OpenAI Vision API requires images as base64 data URLs:
```python
data_url = f"data:{mime_type};base64,{base64_string}"
```
Format: `data:image/jpeg;base64,/9j/4AAQ...`

### Module-Level Service Initialization

Services in [api/routes.py](api/routes.py) are initialized at module level:
```python
openai_service = OpenAIService()
image_service = ImageService()
agent = ProductPhotoAgent(openai_service)
```

This creates singletons that persist across requests. For dependency injection or request-scoped services, use FastAPI's `Depends()`.

### CORS Configuration

Currently allows all origins (`allow_origins=["*"]`) in [main.py](main.py). For production, specify allowed origins explicitly.

### File Upload Limits

Default max upload: 10MB
Allowed types: `.jpg`, `.jpeg`, `.png`, `.webp`

Configure in [config/settings.py](config/settings.py) or override via environment variables.

## Common Gotchas

- **Use `.env.local` not `.env`**: The settings are configured to load from `.env.local` specifically
- **Image optimization is mandatory**: Always call `image_service.optimize_for_api()` before Vision API calls to avoid size/cost issues
- **JSON extraction can fail**: Wrap agent calls in try/except for `ValueError` when LLM returns invalid JSON
- **Stateless limitations**: The `/plan` endpoint requires manually passing product/idea data from `/detect` response since there's no session storage
- **Turkish prompts**: Current prompts are in Turkish; when adding features, maintain language consistency or add i18n support
