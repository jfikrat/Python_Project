import json
from typing import Any
from openai import OpenAI
from config import settings


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature

    def chat_completion(
        self,
        messages: list[dict[str, Any]],
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> str:
        """
        Send a chat completion request to OpenAI.

        Args:
            messages: List of message dictionaries
            temperature: Override default temperature
            max_tokens: Maximum tokens in response

        Returns:
            Response content as string
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or settings.openai_max_tokens,
        )
        return response.choices[0].message.content

    @staticmethod
    def extract_json(text: str) -> dict[str, Any]:
        """
        Extract JSON from text that may contain code fences or extra text.

        Args:
            text: Raw text response from LLM

        Returns:
            Parsed JSON dictionary

        Raises:
            ValueError: If JSON cannot be extracted
        """
        cleaned = text.strip()

        # Remove code fence markers
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            # Skip language identifier if present
            if "\n" in cleaned:
                cleaned = cleaned.split("\n", 1)[1]

        # Find JSON boundaries
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end < start:
            raise ValueError("No valid JSON found in response")

        json_str = cleaned[start:end + 1]
        return json.loads(json_str)
