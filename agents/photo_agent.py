import json
from typing import Any
from services import OpenAIService


class ProductPhotoAgent:
    """
    Agentic workflow for product photo shoot planning.

    Workflow:
    1. Detect product from image (vision)
    2. Generate creative shoot ideas
    3. Create detailed shot plans based on selection
    """

    def __init__(self, openai_service: OpenAIService):
        self.openai = openai_service

    def detect_product(self, image_data_url: str) -> dict[str, Any]:
        """
        Step 1: Detect product from image using vision model.

        Args:
            image_data_url: Base64 data URL of the image

        Returns:
            Dictionary with product details:
            {
                "product": str,
                "category": str,
                "attributes": list[str],
                "confidence": int
            }
        """
        system_msg = {
            "role": "system",
            "content": (
                "You are a precise product identifier for e-commerce photo shoots. "
                "Identify the main product only; ignore people or background clutter. "
                "Return ONLY valid JSON, no additional text."
            ),
        }

        user_msg = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Aşağıdaki fotoğrafta ana ürünü tespit et ve sadece JSON döndür.\n"
                        "Şema:\n"
                        "{\n"
                        '  "product": "kısa ürün ismi",\n'
                        '  "category": "kategori (örn: ayakkabı, kulaklık, çanta)",\n'
                        '  "attributes": ["özellik1", "özellik2", ...],\n'
                        '  "confidence": 85\n'
                        "}\n"
                        "Attributes maksimum 6 adet olsun ve ürünün görsel/fiziksel özelliklerine odaklansın."
                    ),
                },
                {"type": "image_url", "image_url": {"url": image_data_url}},
            ],
        }

        response = self.openai.chat_completion([system_msg, user_msg])
        return self.openai.extract_json(response)

    def suggest_ideas(
        self, product: str, category: str, attributes: list[str]
    ) -> dict[str, Any]:
        """
        Step 2: Generate creative shoot ideas based on product.

        Args:
            product: Product name
            category: Product category
            attributes: List of product attributes

        Returns:
            Dictionary with ideas array:
            {
                "ideas": [
                    {
                        "id": "I1",
                        "title": str,
                        "summary": str,
                        "why_it_works": str,
                        "shot_keywords": list[str]
                    },
                    ...
                ]
            }
        """
        system_msg = {
            "role": "system",
            "content": (
                "You are a creative product photography director. "
                "Generate commercially viable, distinct shoot concepts. "
                "Return ONLY valid JSON, no additional text."
            ),
        }

        user_text = (
            "Ürüne özel 5 farklı çekim fikri öner. Her fikir benzersiz ve ticari açıdan değerli olmalı.\n"
            "Sadece JSON döndür. Şema:\n"
            "{\n"
            '  "ideas": [\n'
            "    {\n"
            '      "id": "I1",\n'
            '      "title": "kısa başlık",\n'
            '      "summary": "fikrin kısa açıklaması",\n'
            '      "why_it_works": "ticari gerekçe",\n'
            '      "shot_keywords": ["anahtar1", "anahtar2", "anahtar3"]\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Ürün: {product}\n"
            f"Kategori: {category}\n"
            f"Özellikler: {', '.join(attributes[:6])}\n"
        )

        user_msg = {"role": "user", "content": user_text}

        response = self.openai.chat_completion([system_msg, user_msg])
        return self.openai.extract_json(response)

    def build_shot_plan(
        self, product: str, selected_idea: dict[str, Any], count: int
    ) -> dict[str, Any]:
        """
        Step 3: Generate detailed shot plans for selected idea.

        Args:
            product: Product name
            selected_idea: The chosen idea dictionary
            count: Number of shots to generate

        Returns:
            Dictionary with shots array:
            {
                "shots": [
                    {
                        "index": 1,
                        "title": str,
                        "camera": {"angle": str, "lens": str, "aperture": str},
                        "lighting": str,
                        "background": str,
                        "props": str,
                        "composition": str,
                        "instructions": str,
                        "gen_prompt": str | None
                    },
                    ...
                ]
            }
        """
        system_msg = {
            "role": "system",
            "content": (
                "You are a senior photo art director with expertise in commercial product photography. "
                "Create detailed, actionable shot plans that are distinct and professionally viable. "
                "Return ONLY valid JSON, no additional text."
            ),
        }

        user_text = (
            "Seçilen fikir için detaylı çekim planları üret. Her plan birbirinden farklı ve profesyonel olmalı.\n"
            "Sadece JSON döndür. Şema:\n"
            "{\n"
            '  "shots": [\n'
            "    {\n"
            '      "index": 1,\n'
            '      "title": "kısa başlık",\n'
            '      "camera": {\n'
            '        "angle": "açı (örn: 45 derece, top-down, eye-level)",\n'
            '        "lens": "lens (örn: 50mm, 85mm)",\n'
            '        "aperture": "diyafram (örn: f/2.8, f/8)"\n'
            "      },\n"
            '      "lighting": "ışıklandırma kurulumu detaylı açıklama",\n'
            '      "background": "arkaplan/ortam detayı",\n'
            '      "props": "aksesuarlar veya none",\n'
            '      "composition": "kompozisyon kuralları",\n'
            '      "instructions": "adım adım çekim talimatları",\n'
            '      "gen_prompt": "opsiyonel: görüntü üretim prompt\'u"\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Ürün: {product}\n"
            f"Seçilen Fikir: {json.dumps(selected_idea, ensure_ascii=False)}\n"
            f"İstenen Adet: {count}\n\n"
            "Her çekim planı benzersiz varyasyon içermeli (açı, ışık, kompozisyon farklılıkları)."
        )

        user_msg = {"role": "user", "content": user_text}

        response = self.openai.chat_completion([system_msg, user_msg])
        return self.openai.extract_json(response)
