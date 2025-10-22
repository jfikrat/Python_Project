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
"""
            # Add model styling guidance if available in template
            if 'model_styling' in template:
                style_guide += f"""
MODEL STYLING GUIDANCE (for this style):
- Model clothing/styling: {template['model_styling']}
- Hair & makeup: {template['model_hair_makeup']}
- Pose & expression: {template['model_pose_direction']}
"""
            style_guide += "\nTüm fikirler bu stil rehberine uygun olmalı.\n"


        # Add model preference guidance
        model_guide = ""
        if model_preference == "with_model":
            model_guide = """
MODEL ZORUNLULUĞU - ÇOK ÖNEMLİ:
- 5 FİKRİN TAMAMINDA İNSAN MODELİ OLMALIDIR
- Her fikir, modelin ürünle aktif etkileşimini ön plana çıkarmalı
- Fikirler model OLMADAN çekilemez olmalı (sadece ürün değil, lifestyle/insanın hikayesi)
- Model sadece aksesuar değil, hikayenin merkezinde olmalı

Zorunlu Çeşitlilik:
- En az 2 farklı cinsiyet perspektifi (kadın/erkek)
- En az 2 farklı yaş grubu (genç yetişkin 20-30 / olgun 35-50)
- Farklı kullanım senaryoları (işe gidiş, alışveriş, gece çıkışı, hafta sonu, seyahat)
- Farklı model-ürün etkileşimleri (omuzda, elde, açık, kapalı, içinden çıkan eşya)

Her Fikrin İçermesi Gerekenler:
- Model karakterizasyonu (yaş, stil, karakter)
- Spesifik senaryo (nerede, ne zaman, neden)
- Model aktivitesi (ne yapıyor, nasıl hissediyor)
- Ürün kullanım şekli (model ürünle nasıl etkileşimde)

Kötü Örnek (model opsiyonel): "Minimalist beyaz arka planda çanta, soft light"
İyi Örnek (model zorunlu): "25 yaşında kadın, sabah işe giderken metrodan inerken, çantayı omuzdan alıp içinden telefon çıkarıyor, acele ve enerji dolu"

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
        # Add category-specific model usage if available and model preference is set
        if 'model_usage' in cat_guide and model_preference == "with_model":
            model_info = cat_guide['model_usage']
            category_guide += f"""
CATEGORY-SPECIFIC MODEL USAGE:
- Importance: {model_info['importance']}
- Recommended shot types:
{chr(10).join(f"  * {shot}" for shot in model_info['shot_types'])}
- Model diversity: {model_info['model_diversity']}
- Styling notes: {model_info['styling_notes']}
- Key angles: {', '.join(model_info['key_angles'])}
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
        self, product: str, selected_idea: dict[str, Any], count: int, model_preference: str = None, model: str = None
    ) -> dict[str, Any]:
        """
        Step 3: Generate image generation prompts for selected idea.

        Args:
            product: Product name
            selected_idea: The chosen idea dictionary
            count: Number of prompts to generate
            model_preference: Optional model preference ('with_model' or 'without_model')
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

        # Build model guidance section
        model_guide = ""
        if model_preference == "with_model":
            model_guide = """
MODELLİ ÇEKİM REHBERİ:
gen_prompt içinde aşağıdaki alanları MUTLAKA ekle:
1. Model Tipi: cinsiyet ve yaş aralığı (örn: "25-30 year old woman", "mature male model")
2. Model Styling: kıyafet tarzı, renk paleti, aksesuarlar (örn: "wearing elegant black dress", "casual denim and white shirt")
3. Saç & Makyaj: saç stili ve makyaj tarifi (örn: "sleek updo, natural makeup", "messy bun, bold red lips")
4. İfade & Poz: yüz ifadesi, duruş, hareket (örn: "confident stance, slight smile", "relaxed pose, looking away")
5. Ürünle Etkileşim: model ürünü nasıl tutuyor/kullanıyor (örn: "holding bag elegantly by handle", "wearing watch on left wrist")
6. Kamera Açısı: kadraj tipi (örn: "half-body shot", "close-up portrait", "full-body environmental")
7. Ortam & Atmosfer: çekim ortamı ve mood (örn: "upscale urban cafe, warm afternoon light", "minimalist studio, dramatic shadows")

ÇEŞİTLİLİK ZORUNLULUĞU - HER SHOT FARKLI OLMALI:

Cinsiyet Dağılımı (istenen shot sayısına göre dengele):
- En az 1 erkek model (örn: "35 year old man", "young male professional")
- En az 1 kadın model (örn: "28 year old woman", "mature female")
- Gerisi mix olabilir

Yaş Çeşitliliği (istenen shot sayısına göre):
- Young adult: 20-28 (örn: "22 year old", "mid-twenties")
- Professional: 28-40 (örn: "30-35 year old", "mature professional")
- Mature: 40+ (örn: "45 year old", "mature elegant")

Etnik/Fiziksel Çeşitlilik:
- Farklı ten renkleri belirt (light skin, medium skin tone, dark skin)
- Farklı saç tipleri (straight, wavy, curly, textured)
- Farklı vücut tipleri ima edilebilir (tall slender, athletic, curvy)

Stil Varyasyonu (HER SHOT FARKLI OLMALI):
Shot 1: Professional/business (suit, blazer, corporate)
Shot 2: Casual/everyday (jeans, sweater, relaxed)
Shot 3: Elegant/upscale (dress, refined, sophisticated)
Shot 4: Urban/edgy (streetwear, modern, bold)
Shot 5+: Creative/unique (artistic, eclectic, personalized)

Her prompt'ta model açıklaması ŞU FORMATTA OLMALI:
"[age range] year old [gender], [ethnicity/skin tone], [hair type & style], [clothing style], [expression & activity]"

Örnek: "28-32 year old woman, medium skin tone, sleek straight black hair in ponytail, wearing minimalist grey blazer and white shirt, confident smile while checking phone"
"""
        elif model_preference == "without_model":
            model_guide = """
SADECE ÜRÜN ODAKLI ÇEKİM:
- Model veya insan unsuru KULLANMA
- Ürünü flatlay, tabletop veya stilize kompozisyonlarla göster
- Ürün detaylarını ve özelliklerini vurgula
- Props ve dekoratif elementlerle kompozisyon oluştur
"""

        # Add camera language variations for technical diversity
        camera_guide = """
KAMERA & TEKNİK ÇEŞİTLİLİK:
gen_prompt içinde profesyonel fotoğrafçılık terminolojisi kullan. Her shot farklı olmalı:

Lens Seçenekleri (her shot'ta farklı lens belirt):
- 50mm f/1.8 (klasik portre, doğal perspektif)
- 85mm f/1.4 (sıkıştırılmış bokeh, portre)
- 35mm f/2 (environmental, context)
- 24mm f/2.8 (geniş açı, lifestyle)
- 100mm macro f/2.8 (ürün detay, texture)
- 24-70mm f/2.8 (versatile, commercial)

Diyafram (depth of field için):
- f/1.4, f/1.8 (shallow DOF, dreamy bokeh)
- f/2.8, f/4 (balanced, lifestyle)
- f/8, f/11 (sharp, product detail)

Işık Teknikleri (çeşitli kombinasyonlar):
- Soft diffused window light
- Rembrandt lighting (45° açılı, dramatic shadow)
- Butterfly lighting (overhead soft, flattering)
- Rim/edge lighting (arka ışık, product outline)
- Split lighting (profile, dramatic half-face)
- Natural golden hour light
- Studio strobe with softbox
- Continuous LED panel
- Hard directional light (shadows)
- Ambient + fill combination

Kamera Açıları (varyasyon şart):
- Eye-level/straight-on
- Overhead/flat lay (90°)
- Low angle (dramatic, powerful)
- High angle (editorial, documentary)
- 3/4 view (classic product)
- Dutch angle/tilted (dynamic)
- Close-up/macro
- Environmental wide shot

Kompozisyon Terimleri:
- Rule of thirds
- Center framed
- Negative space emphasis
- Tight crop
- Environmental context
- Leading lines
- Symmetrical composition
- Asymmetrical balance

Kalite Anahtar Kelimeleri (her prompt'ta ekle):
- "professional product photography"
- "commercial photography"
- "high resolution, sharp focus"
- "studio lighting" veya "natural light"
- "shallow depth of field" veya "tack sharp"
- "clean background" veya "environmental setting"
"""

        # Add storytelling triggers for narrative-driven prompts
        story_guide = """
HİKAYE ANLATIMI & ATMOSFER:
Her gen_prompt sadece teknik tarif değil, bir hikaye anlatmalı. Aşağıdaki elementleri kullan:

Zaman & Atmosfer (birini seç):
- "early morning light, fresh start energy"
- "golden hour sunset, warm nostalgic mood"
- "midday bright, energetic vibrant"
- "blue hour twilight, elegant mysterious"
- "overcast soft light, calm contemplative"
- "late afternoon, relaxed weekend vibe"

Duygusal Ton (her shot farklı):
- Confident & powerful
- Elegant & sophisticated
- Playful & spontaneous
- Calm & minimal
- Luxurious & aspirational
- Urban & edgy
- Warm & inviting
- Bold & dramatic

Senaryo/Context (model varsa):
- Commuting to work (bag on shoulder, city background)
- Weekend cafe moment (relaxed, latte on table)
- Evening event arrival (dressed up, confident stride)
- Shopping trip (browsing, casual joy)
- Travel departure (airport, excitement)
- Park stroll (natural, carefree)
- Office to dinner transition (versatile styling)
- Art gallery visit (cultured, thoughtful)

Detay Vurgusu (her shot 1-2 tanesini öne çıkar):
- Texture closeup (suede, leather grain)
- Hardware detail (zipper, buckle, clasp)
- Stitching & craftsmanship
- Shape & silhouette
- How it sits/hangs when worn
- Interior organization (open bag shot)
- Size comparison (next to common object)
- Color richness in different light

Prompt Yapısı Örneği:
"[MODEL DESCRIPTION], [PRODUCT INTERACTION], [SCENARIO/CONTEXT], [LIGHTING], [CAMERA SPECS], [EMOTIONAL TONE], [COMPOSITION], professional product photography, high resolution"

Örnek:
"25-30 year old woman in minimalist beige trench coat, holding brown suede hobo bag casually by handle, walking through modern glass lobby, soft diffused morning light from floor-to-ceiling windows, shot with 50mm f/2, calm confident energy, rule of thirds composition, professional product photography, sharp focus, shallow depth of field"
"""

        user_text = (
            "Seçilen fikir için görüntü üretim promptları oluştur. Her prompt birbirinden farklı ve etkili olmalı.\n"
            f"{model_guide}\n"
            f"{camera_guide}\n"
            f"{story_guide}\n"
            "Sadece JSON döndür. Şema:\n"
            "{\n"
            '  "shots": [\n'
            "    {\n"
            '      "index": 1,\n'
            '      "title": "kısa başlık",\n'
            '      "style_description": "stil ve estetik açıklaması",\n'
            '      "gen_prompt": "detaylı görüntü üretim prompt\'u (İngilizce, DALL-E/Midjourney formatında)",\n'
            '      "camera_details": "optional - kamera spesifikasyonları (örn: 50mm f/2.8, eye-level angle)",\n'
            '      "negative_prompt": "optional - görüntüde olmaması gerekenler (örn: blurry, low quality, distorted)",\n'
            '      "key_props": ["optional - array of key props/elements in shot"],\n'
            '      "post_processing": "optional - önerilen post processing (örn: warm color grade, high contrast)",\n'
            '      "story_element": "optional - bu shot\'ın hikayedeki rolü (örn: establishing mood, showing product detail)"\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Ürün: {product}\n"
            f"Seçilen Fikir: {json.dumps(selected_idea, ensure_ascii=False)}\n"
            f"İstenen Adet: {count}\n\n"
            "Her prompt benzersiz açı, stil, ışık ve kompozisyon içermeli. "
            "gen_prompt alanı İngilizce ve çok detaylı olmalı (ürün detayı, açı, ışık, ortam, stil, kalite anahtar kelimeleri).\n\n"
            "ENRICHED FIELDS GUIDANCE:\n"
            "- camera_details: Extract camera specs from gen_prompt (lens, aperture, angle)\n"
            "- negative_prompt: List what to avoid (blurry, distorted, low quality, extra limbs, bad anatomy, etc.)\n"
            "- key_props: List 2-4 important props mentioned in the shot\n"
            "- post_processing: Suggest color grading or editing style (warm tones, high contrast, matte finish, etc.)\n"
            "- story_element: Explain this shot's narrative purpose (establishing environment, showing detail, conveying emotion, etc.)\n"
        )

        user_msg = {"role": "user", "content": user_text}

        response = await self.openai.chat_completion([system_msg, user_msg], model=model)
        return self.openai.extract_json(response)
