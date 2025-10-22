import json
import re
import logging
from typing import Any
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API (async)."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature

    async def chat_completion(
        self,
        messages: list[dict[str, Any]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        model: str | None = None
    ) -> str:
        """
        Send an async chat completion request to OpenAI.

        Args:
            messages: List of message dictionaries
            temperature: Override default temperature
            max_tokens: Maximum tokens in response
            model: Override default model (e.g., "gpt-5-mini")

        Returns:
            Response content as string
        """
        selected_model = model or self.model

        # GPT-5 and o-series models have different API requirements
        uses_new_api = selected_model.startswith(('gpt-5', 'o3', 'o4'))

        completion_params = {
            "model": selected_model,
            "messages": messages,
        }

        # GPT-5 and o-series models only support default temperature (1.0)
        if not uses_new_api:
            completion_params["temperature"] = temperature or self.temperature

        # Use appropriate token parameter based on model
        if uses_new_api:
            # Reasoning models need MORE tokens (they use tokens for reasoning + response)
            # Regular models use 4000, reasoning models need at least 16000
            reasoning_tokens = max_tokens or 16000  # Much higher for reasoning models
            completion_params["max_completion_tokens"] = reasoning_tokens

            # Set reasoning effort to minimal for speed and cost efficiency
            # Options: minimal, low, medium (default), high
            # minimal = very fast, very few reasoning tokens
            completion_params["reasoning_effort"] = "low"
        else:
            completion_params["max_tokens"] = max_tokens or settings.openai_max_tokens

        response = await self.client.chat.completions.create(**completion_params)
        content = response.choices[0].message.content

        # Log and handle empty responses with automatic fallback
        if not content or not content.strip():
            fallback_model = "gpt-4o-mini"

            # If user already tried the fallback model, don't retry
            if selected_model == fallback_model:
                logger.error(
                    f"Empty response from fallback model '{selected_model}'. "
                    f"Response object: {response}"
                )
                raise ValueError(
                    f"Model '{selected_model}' returned an empty response. "
                    f"Please check your OpenAI API key and quota."
                )

            # Try fallback model automatically
            logger.warning(
                f"Model '{selected_model}' returned empty response. "
                f"Automatically falling back to '{fallback_model}'..."
            )

            # Reconstruct params for fallback model (use legacy API params)
            fallback_params = {
                "model": fallback_model,
                "messages": messages,
                "temperature": temperature or self.temperature,
                "max_tokens": max_tokens or settings.openai_max_tokens
            }

            response = await self.client.chat.completions.create(**fallback_params)
            content = response.choices[0].message.content

            if not content or not content.strip():
                raise ValueError(
                    f"Both '{selected_model}' and fallback model '{fallback_model}' "
                    f"returned empty responses. Please check your OpenAI API configuration."
                )

            logger.info(f"Successfully used fallback model '{fallback_model}'")

        return content

    @staticmethod
    def extract_json(text: str) -> dict[str, Any]:
        """
        Extract JSON from text that may contain code fences or extra text.

        Args:
            text: Raw text response from LLM

        Returns:
            Parsed JSON dictionary

        Raises:
            ValueError: If JSON cannot be extracted or parsed
        """
        if not text or not text.strip():
            raise ValueError("Empty response from LLM")

        cleaned = text.strip()

        # Try to extract from code fences using regex (handles language identifiers)
        code_fence_pattern = r'```(?:json)?\s*\n?(.*?)```'
        code_fence_match = re.search(code_fence_pattern, cleaned, re.DOTALL)
        if code_fence_match:
            cleaned = code_fence_match.group(1).strip()

        # Find JSON boundaries (handles nested objects)
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end < start:
            raise ValueError(
                "No valid JSON object found in response. "
                "Make sure the LLM returns a JSON object enclosed in curly braces."
            )

        json_str = cleaned[start:end + 1]

        # Try to parse JSON with informative error messages
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format at line {e.lineno}, column {e.colno}: {e.msg}. "
                f"Extracted string: {json_str[:100]}..."
            )
