import json
from typing import Any
from services import OpenAIService
from config.style_templates import get_style_template, get_category_guidelines


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

    async def detect_product(self, image_data_url: str, model: str = None) -> dict[str, Any]:
        """
        Step 1: Detect product from image using vision model.

        Args:
            image_data_url: Base64 data URL of the image
            model: Optional AI model to use (overrides default)

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

        response = await self.openai.chat_completion([system_msg, user_msg], model=model)
        return self.openai.extract_json(response)

    async def suggest_ideas(
        self, product: str, category: str, attributes: list[str], style: str = None, model_preference: str = None, model: str = None
    ) -> dict[str, Any]:
        """
        Step 2: Generate creative shoot ideas based on product, style, and model preference.

        Args:
            product: Product name
            category: Product category
            attributes: List of product attributes
            style: Optional style key (minimal, luxury, lifestyle, decorative, etc.)
            model_preference: Optional model preference ('with_model' or 'without_model')
            model: Optional AI model to use (overrides default)

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
        # Get style template if provided
        style_guide = ""
        if style:
            template = get_style_template(style)
            style_guide = f"""
STYLE GUIDELINES ({template['name_tr']}):
- Ton: {template['tone']}
- Aydınlatma: {template['lighting']}
- Arka plan: {template['background']}
- Aksesuarlar: {template['props']}
- Anahtar kelimeler: {', '.join(template['keywords'])}

Tüm fikirler bu stil rehberine uygun olmalı.
"""

        # Add model preference guidance
        model_guide = ""
        if model_preference == "with_model":
            model_guide = """
MODEL PREFERENCE:
- Çekimlerde İNSAN MODELİ kullan
- Modelin ürünü nasıl kullandığını veya taşıdığını göster
- Lifestyle çekimler öner (model ürünle etkileşimde)
- Eller, gövde veya tam vücut gösterilebilir
- Gerçek kullanım senaryolarını vurgula

"""
        elif model_preference == "without_model":
            model_guide = """
MODEL PREFERENCE:
- Çekimlerde İNSAN MODELİ KULLANMA
- Sadece ürün odaklı çekimler öner
- Ürünü stillize et, dekore et veya kompozisyon içine yerleştir
- Flatlay, tabletop veya product-only setup'lar kullan
- Ürün detaylarını ve özelliklerini öne çıkar

"""

        # Get category guidelines
        cat_guide = get_category_guidelines(category)
        category_guide = f"""
KATEGORI BEST PRACTICES ({category}):
- Odak noktası: {cat_guide['focus']}
- Gösterilmesi gerekenler: {', '.join(cat_guide['must_show'])}
- Kaçınılması gerekenler: {cat_guide['avoid']}
"""

        system_msg = {
            "role": "system",
            "content": (
                "You are a creative product photography director. "
                "Generate commercially viable, distinct shoot concepts following the given guidelines. "
                "Return ONLY valid JSON, no additional text."
            ),
        }

        user_text = (
            "Ürüne özel 5 farklı çekim fikri öner. Her fikir benzersiz ve ticari açıdan değerli olmalı.\n"
            f"{style_guide}\n"
            f"{model_guide}\n"
            f"{category_guide}\n"
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

        response = await self.openai.chat_completion([system_msg, user_msg], model=model)
        return self.openai.extract_json(response)

    async def build_shot_plan(
        self, product: str, selected_idea: dict[str, Any], count: int, model: str = None
    ) -> dict[str, Any]:
        """
        Step 3: Generate image generation prompts for selected idea.

        Args:
            product: Product name
            selected_idea: The chosen idea dictionary
            count: Number of prompts to generate
            model: Optional AI model to use (overrides default)

        Returns:
            Dictionary with shots array:
            {
                "shots": [
                    {
                        "index": 1,
                        "title": str,
                        "style_description": str,
                        "gen_prompt": str
                    },
                    ...
                ]
            }
        """
        system_msg = {
            "role": "system",
            "content": (
                "You are an expert AI image generation prompt engineer specializing in product photography. "
                "Create detailed, effective prompts for tools like DALL-E, Midjourney, or Stable Diffusion. "
                "Return ONLY valid JSON, no additional text."
            ),
        }

        user_text = (
            "Seçilen fikir için görüntü üretim promptları oluştur. Her prompt birbirinden farklı ve etkili olmalı.\n"
            "Sadece JSON döndür. Şema:\n"
            "{\n"
            '  "shots": [\n'
            "    {\n"
            '      "index": 1,\n'
            '      "title": "kısa başlık",\n'
            '      "style_description": "stil ve estetik açıklaması (örn: minimalist beyaz arka plan, dramatic lighting)",\n'
            '      "gen_prompt": "detaylı görüntü üretim prompt\'u (İngilizce, DALL-E/Midjourney formatında)"\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Ürün: {product}\n"
            f"Seçilen Fikir: {json.dumps(selected_idea, ensure_ascii=False)}\n"
            f"İstenen Adet: {count}\n\n"
            "Her prompt benzersiz açı, stil, ışık ve kompozisyon içermeli. "
            "gen_prompt alanı İngilizce ve çok detaylı olmalı (ürün detayı, açı, ışık, ortam, stil, kalite anahtar kelimeleri)."
        )

        user_msg = {"role": "user", "content": user_text}

        response = await self.openai.chat_completion([system_msg, user_msg], model=model)
        return self.openai.extract_json(response)
