# Gemini 2.5 Flash Image ("Nano Banana") Integration Notes

## Overview
- Gemini 2.5 Flash Image is Google DeepMind’s latest multimodal image generation and editing model, positioned as the “Nano Banana” release and currently in public preview with production usage allowed. It focuses on maintaining subject identity, prompt-driven editing, and multimodal reasoning that mixes Gemini’s language understanding with image output.[^blog]
- The model is exposed through the Gemini API (`model: gemini-2.5-flash-image`), Google AI Studio playgrounds, and enterprise channels such as Vertex AI. Partners like OpenRouter and fal.ai also surface the model for developers.[^blog]
- Every generated or edited image is stamped with an invisible SynthID watermark so downstream systems can flag the media as AI-created.[^blog]

## Key Capabilities
- **Character & product consistency** across multiple generation calls without losing visual identity, useful for avatars, brand assets, and catalog imagery.[^blog]
- **Prompt-based fine editing** lets text instructions add, remove, or retouch objects (pose changes, background swaps, stain removal) without manual masks.[^blog]
- **World-knowledge reasoning** combines image understanding and Gemini’s language model to follow complex instructions (e.g., interpreting diagrams or answering contextual questions).[^blog]
- **Multi-image fusion** accepts up to three reference images to blend scenes, restyle interiors, or transfer textures.[^image-doc]
- **Conversational refinement** supports iterative editing in a single session, keeping context over turns.[^image-doc]

## Pricing & Quotas (Gemini API, Paid Tier)
- Output billing is flat: each generated image consumes 1,290 output tokens (≤1024×1024) priced at $30 per 1M tokens → $0.039 per image.[^pricing]
- Text or image inputs are billed at $0.30 per 1M tokens. (No free tier for the native image model; sandbox access remains via AI Studio.)[^pricing]
- Free AI Studio sessions are rate-limited (historically 500 requests/day shared with other Flash models); upgrade to paid keys for higher and production-grade limits.[^pricing]
- Grounding features (Google Search/Maps) share request-per-day quotas with other Flash models; exceeding the shared free pool costs $35 per 1,000 grounded prompts.[^pricing]

## Access & Authentication Path
1. **Create a Gemini API key** in Google AI Studio (free tier) or provision through Google Cloud for Vertex AI if enterprise security/compliance is required.
2. **Choose environment**:
   - *Direct Gemini API*: use Google’s official SDKs (`google-genai` for Python/Node) or REST with bearer token auth.
   - *AI Studio build mode*: rapid prototyping with deploy/share options. Useful before wiring into the app UI.[^blog]
   - *Vertex AI*: integrates with existing GCP projects, IAM, and monitoring; necessary for SLAs or private networking.
   - *Third-party gateways*: OpenRouter/fal.ai offer managed quotas or pay-as-you-go alternatives (verify data-processing policies).[^blog]
3. **Store key securely** (server-side); do not expose in front-end clients. If our chat app needs client-side generation, proxy requests through our backend.

## Request Basics (Gemini API)
```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "Ultra-realistic portrait of our mascot holding a nano banana in the app’s color palette"

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["Image"],
        image_config=types.ImageConfig(aspect_ratio="4:5"),
    ),
)

image_bytes = response.candidates[0].content.parts[0].inline_data.data
# Persist image_bytes (base64) or convert to PNG before returning to clients
```
- `contents` may include text prompts, existing images (PIL objects or base64/URL references), or multi-turn history. Each additional image counts toward input tokens and reduces max payload size.[^image-doc]
- `response_modalities` can restrict output to images only if text metadata is unnecessary.[^image-doc]
- Aspect ratios supported: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9. All variants still consume 1,290 tokens/image.[^image-doc]

## Editing & Multi-Image Composition
- To perform edits, include the base image(s) and a text instruction in `contents`. The model matches original lighting and style automatically.[^image-doc]
- Semantic “masking” is conversation-based: describe the region to change (“replace the billboard text with…”) rather than uploading explicit alpha masks.[^image-doc]
- Multi-image calls blend up to three inputs; use for style transfer (e.g., apply mood board to product shots) or scene staging (drag product image into a room).[^^???]

## Prompting Playbook
- Prefer descriptive sentences over keyword lists; explain subject, context, intent, and output use case.[^image-doc]
- Reference photographic terms (lens, lighting, focus) for photorealism or specify illustration styles for logos, stickers, and comics.[^image-doc]
- Iterate conversationally: adjust lighting, expression, or layout with follow-up prompts rather than regenerating from scratch.[^image-doc]
- Positive phrasing (“an empty plaza with no vehicles”) guides the scene better than negative keywords.[^image-doc]
- For on-image typography, generate the text separately first, then request the combined layout to improve fidelity.[^image-doc]

## Limitations & Safety
- Works best in English, Spanish (MX), Japanese, Simplified Chinese, and Hindi prompts.[^image-doc]
- Maximum three reference images per call; larger batches should be processed sequentially.[^image-doc]
- Currently cannot process uploads depicting children for users in EEA/CH/UK.[^image-doc]
- Rejects disallowed content per Google’s Prohibited Use Policy; ensure downstream moderation aligns with Gemini API terms.[^image-doc]
- Each response includes SynthID watermark; warn users that edits remain detectable.[^blog]
- Image generation/editing does not accept audio/video inputs and will not always honor requested image counts exactly.[^image-doc]

## Implementation Considerations for Our Chat App
- Route generation requests through our backend service to keep API keys secret and add domain-level guardrails (prompt filtering, usage quotas).
- Cache or deduplicate prompts to control costs; each render is a flat $0.039, so batch replays can spike spend quickly.
- Provide UX affordances for iterative edits (send follow-up prompts referencing the last image) to leverage the model’s conversational memory while minimizing full regenerations.
- Store outputs as binary images rather than long base64 strings in chat history to reduce payload sizes.
- Log prompt/image pairs securely for audit and to comply with Google’s policies about sensitive data handling.

## Next Steps
- Prototype flows in Google AI Studio build mode to validate UX with real prompts.
- Implement backend proxy endpoint that wraps `generate_content`, supporting both creation and edits plus optional aspect-ratio selection.
- Evaluate cost controls (per-user quotas, usage alerts) before rolling out to production.
- Prepare communications around AI-generated media, including disclosure of SynthID watermark and moderation guidelines.

## References
- [^blog]: “Introducing Gemini 2.5 Flash Image, our state-of-the-art image model,” Google Developers Blog, 26 Aug 2025. Retrieved via r.jina.ai mirror.
- [^image-doc]: “Image generation with Gemini (aka Nano Banana)” Gemini API documentation, accessed via r.jina.ai mirror.
- [^pricing]: “Gemini Developer API Pricing,” Gemini API documentation, accessed via r.jina.ai mirror.
