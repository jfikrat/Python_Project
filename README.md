# Product Photo Agent API

AI-powered agentic workflow for product photo shoot planning using OpenAI.

## Features

- **Product Detection**: Upload a product image to automatically identify product name, category, and attributes
- **Creative Ideas**: Get 5 professional shoot concept suggestions tailored to your product
- **Shot Planning**: Generate detailed, actionable photography plans with camera settings, lighting, composition, and step-by-step instructions

## Architecture

```
Python_Project/
├── agents/          # Agentic workflow logic
├── services/        # OpenAI & image processing
├── api/             # FastAPI routes & Pydantic models
├── config/          # Settings & environment
└── main.py          # Application entry point
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/cglabs/ai-projects/Python_Project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify `.env.local` exists with your OpenAI API key:**
   ```
   OPENAI_API_KEY=sk-proj-...
   ```

## Usage

### Start the API Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI to test endpoints interactively.

### API Endpoints

#### 1. Detect Product & Get Ideas

**Endpoint:** `POST /api/detect`

**Description:** Upload a product image to detect the product and receive 5 creative shoot ideas.

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/product.jpg"
```

**Response:**
```json
{
  "product": "Nike Air Max 90",
  "category": "ayakkabı",
  "attributes": ["spor", "beyaz", "mesh", "rahat"],
  "confidence": 95,
  "ideas": [
    {
      "id": "I1",
      "title": "Dynamic Motion Shot",
      "summary": "Ayakkabıyı hareket halinde göster",
      "why_it_works": "Ürünün spor özelliğini vurgular",
      "shot_keywords": ["action", "energy", "athletic"]
    }
  ]
}
```

#### 2. Generate Shot Plans

**Endpoint:** `POST /api/plan`

**Description:** Generate detailed shot plans based on a selected idea.

**Request Body:**
```json
{
  "product": "Nike Air Max 90",
  "idea_id": "I1",
  "count": 5
}
```

**cURL Example:**
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

**Response:**
```json
{
  "shots": [
    {
      "index": 1,
      "title": "Hero Angle",
      "camera": {
        "angle": "45 derece",
        "lens": "50mm",
        "aperture": "f/2.8"
      },
      "lighting": "Softbox sol, rim light sağ",
      "background": "Beyaz seamless",
      "props": "Koşu bandı",
      "composition": "Diagonal leading lines",
      "instructions": "1. Ayakkabıyı 45 derece açıyla yerleştir...",
      "gen_prompt": "white sneaker on treadmill, 45 degree angle, soft lighting"
    }
  ]
}
```

#### 3. Health Check

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Product Photo Agent API"
}
```

## Workflow

```
1. User uploads product photo
   ↓
2. AI detects product details (GPT-4o-mini Vision)
   ↓
3. AI generates 5 creative shoot ideas
   ↓
4. User selects an idea & specifies shot count
   ↓
5. AI generates detailed shot plans
   ↓
6. User receives actionable photography instructions
```

## Configuration

Edit [config/settings.py](config/settings.py) or set environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: `gpt-4o-mini`)
- `OPENAI_TEMPERATURE`: Creativity level (default: `0.4`)
- `MAX_UPLOAD_SIZE`: Max image size in bytes (default: `10MB`)
- `ALLOWED_IMAGE_TYPES`: Supported formats (default: `.jpg, .jpeg, .png, .webp`)

## Development

### Run with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure:

- **agents/photo_agent.py**: Core agentic logic (3-step workflow)
- **services/openai_service.py**: OpenAI API wrapper
- **services/image_service.py**: Image validation & processing
- **api/models.py**: Pydantic schemas for requests/responses
- **api/routes.py**: FastAPI endpoint definitions
- **config/settings.py**: Environment configuration

## Notes

- This is a **stateless** API (no session storage)
- For production, implement proper CORS origins in [main.py](main.py)
- The `/plan` endpoint currently requires manually passing the `idea_id` from `/detect` response

## License

MIT
