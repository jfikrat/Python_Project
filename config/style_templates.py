"""
Style templates for photo shoot ideas.
Each style defines guidelines for lighting, background, props, and tone.
"""

STYLE_TEMPLATES = {
    "minimal": {
        "name": "Minimal & Modern",
        "name_tr": "Minimalist & Modern",
        "tone": "clean, simple, focused on product details",
        "lighting": "soft diffused light, no harsh shadows, even illumination",
        "background": "solid colors (white, gray, pastel) or simple textures",
        "props": "minimal or none, only if essential",
        "composition": "centered, negative space, rule of thirds",
        "keywords": ["minimalist", "clean", "simple", "focused", "modern", "sleek"],
        "description_tr": "Sade bir masa üzerinde, minimal bir arka plan ile, ürünün detaylarını ön plana çıkaracak şekilde"
    },

    "luxury": {
        "name": "Luxury & Premium",
        "name_tr": "Lüks & Premium",
        "tone": "elegant, sophisticated, high-end, premium quality",
        "lighting": "dramatic lighting, high contrast, golden hour, rim lighting",
        "background": "marble, velvet, silk, premium materials, dark moody backgrounds",
        "props": "gold/silver accents, premium accessories, elegant items",
        "composition": "dramatic angles, depth, layered composition",
        "keywords": ["luxurious", "elegant", "premium", "high-end", "sophisticated", "exclusive"],
        "description_tr": "Mermer zemin veya kadife kumaş üzerinde, altın aksesuarlar ile, dramatik aydınlatma"
    },

    "lifestyle": {
        "name": "Lifestyle & Natural",
        "name_tr": "Yaşam Tarzı & Doğal",
        "tone": "natural, relatable, authentic, everyday use",
        "lighting": "natural light, warm tones, golden hour, soft shadows",
        "background": "real-life settings (home, cafe, outdoor, office)",
        "props": "everyday items, hands in action, people using product",
        "composition": "candid shots, natural poses, environmental context",
        "keywords": ["lifestyle", "natural", "relatable", "authentic", "everyday", "real-life"],
        "description_tr": "Gerçek hayat ortamında, doğal ışıkta, kullanım anında veya günlük hayattan bir sahne"
    },

    "vintage": {
        "name": "Vintage & Retro",
        "name_tr": "Vintage & Retro",
        "tone": "nostalgic, timeless, classic, retro aesthetics",
        "lighting": "warm tones, slightly muted colors, film-like quality",
        "background": "aged textures, old wood, vintage paper, rustic materials",
        "props": "vintage items, retro accessories, old cameras, books",
        "composition": "centered, symmetrical, classic framing",
        "keywords": ["vintage", "retro", "nostalgic", "classic", "timeless", "heritage"],
        "description_tr": "Eski ahşap masa üzerinde, vintage aksesuarlar ile, retro bir atmosferde"
    },

    "bold": {
        "name": "Bold & Vibrant",
        "name_tr": "Cesur & Canlı",
        "tone": "energetic, eye-catching, bold, vibrant",
        "lighting": "bright, saturated colors, high key lighting",
        "background": "bright solid colors, geometric patterns, contrasting backgrounds",
        "props": "colorful items, bold accessories, contrasting elements",
        "composition": "dynamic angles, asymmetric, creative framing",
        "keywords": ["bold", "vibrant", "colorful", "energetic", "dynamic", "eye-catching"],
        "description_tr": "Parlak renkli arka plan ile, cesur kompozisyon, canlı ve dikkat çekici"
    },

    "industrial": {
        "name": "Industrial & Urban",
        "name_tr": "Endüstriyel & Kentsel",
        "tone": "raw, edgy, urban, modern industrial",
        "lighting": "hard light, dramatic shadows, warehouse lighting",
        "background": "concrete, metal, brick walls, industrial settings",
        "props": "metal objects, tools, urban elements",
        "composition": "strong lines, geometric shapes, architectural elements",
        "keywords": ["industrial", "urban", "raw", "edgy", "modern", "gritty"],
        "description_tr": "Beton veya tuğla duvar önünde, sert aydınlatma, endüstriyel bir atmosferde"
    },

    "decorative": {
        "name": "Decorative & Artistic",
        "name_tr": "Dekoratif & Sanatsal",
        "tone": "artistic, aesthetic, visually pleasing, product as art piece",
        "lighting": "soft natural light, artistic shadows, creative use of light and shadow",
        "background": "aesthetic compositions, flowers, fabrics, artistic arrangements",
        "props": "decorative elements (flowers, ribbons, fabrics, books, candles), aesthetic items",
        "composition": "flatlay, overhead shots, artistic arrangements, symmetrical or asymmetrical balance",
        "keywords": ["decorative", "artistic", "aesthetic", "flatlay", "composed", "beautiful"],
        "description_tr": "Dekoratif düzenleme ile, çiçekler ve estetik objeler arasında, sanat eseri gibi sunulmuş"
    },

    "white_background": {
        "name": "White Background",
        "name_tr": "Beyaz Arka Plan",
        "tone": "professional, clean, e-commerce standard",
        "lighting": "bright, even lighting, no shadows",
        "background": "pure white background (#FFFFFF), seamless backdrop",
        "props": "none, product only",
        "composition": "centered, product fills frame, multiple angles",
        "keywords": ["white background", "clean", "professional", "ecommerce", "catalog"],
        "description_tr": "Tamamen beyaz arka planda, profesyonel stüdyo çekimi, sadece ürün odaklı"
    },

    "flatlay": {
        "name": "Flat Lay",
        "name_tr": "Yukarıdan Düzenleme",
        "tone": "organized, aesthetic, overhead perspective",
        "lighting": "even overhead lighting, soft shadows",
        "background": "flat surface (wood, marble, fabric, paper)",
        "props": "complementary items arranged aesthetically",
        "composition": "overhead 90-degree angle, symmetrical or asymmetrical arrangement",
        "keywords": ["flatlay", "overhead", "arrangement", "organized", "top-down"],
        "description_tr": "Düz bir yüzey üzerine estetik olarak yerleştirilmiş, yukarıdan çekilmiş"
    },

    "editorial": {
        "name": "Editorial",
        "name_tr": "Editorial (Dergi Tarzı)",
        "tone": "storytelling, aspirational, magazine-quality, brand essence",
        "lighting": "creative lighting, dramatic or soft depending on story",
        "background": "conceptual settings, themed environments",
        "props": "storytelling elements, thematic accessories",
        "composition": "creative angles, narrative-driven, artistic framing",
        "keywords": ["editorial", "magazine", "storytelling", "aspirational", "brand"],
        "description_tr": "Dergi çekimi tarzında, hikaye anlatan, marka ruhunu yansıtan sahneler"
    },

    "studio_clean": {
        "name": "Clean Studio",
        "name_tr": "Temiz Stüdyo",
        "tone": "professional, polished, high-quality",
        "lighting": "controlled studio lighting, softboxes, no harsh shadows",
        "background": "neutral colors (white, gray, beige), simple backdrop",
        "props": "minimal, professional setup",
        "composition": "clean lines, professional framing, technical precision",
        "keywords": ["studio", "professional", "clean", "controlled", "polished"],
        "description_tr": "Profesyonel stüdyo ortamında, kontrollü aydınlatma ile çekilmiş"
    },

    "dark_moody": {
        "name": "Dark & Moody",
        "name_tr": "Koyu & Dramatik",
        "tone": "mysterious, dramatic, premium, atmospheric",
        "lighting": "low-key lighting, dramatic shadows, chiaroscuro",
        "background": "dark backgrounds (black, charcoal, deep tones)",
        "props": "dark elegant items, moody accessories",
        "composition": "dramatic angles, strong contrast, depth",
        "keywords": ["dark", "moody", "dramatic", "mysterious", "low-key"],
        "description_tr": "Koyu arka planda, dramatik gölgeler ve atmosferik bir ruh hali ile"
    },

    "colorful_pop": {
        "name": "Colorful & Pop",
        "name_tr": "Renkli & Pop",
        "tone": "vibrant, energetic, playful, eye-catching",
        "lighting": "bright, saturated, high-key lighting",
        "background": "bold solid colors, neon, pastels, colorful gradients",
        "props": "colorful accessories, playful elements",
        "composition": "dynamic, fun, unconventional angles",
        "keywords": ["colorful", "vibrant", "pop", "playful", "bright"],
        "description_tr": "Parlak renkli arka planlar ile, eğlenceli ve dikkat çekici kompozisyonlar"
    },

    "natural_light": {
        "name": "Natural Light",
        "name_tr": "Doğal Işık",
        "tone": "authentic, soft, organic, genuine",
        "lighting": "window light, golden hour, soft natural shadows",
        "background": "natural settings, home environments, simple backdrops",
        "props": "natural materials, organic elements",
        "composition": "soft, natural, candid feel",
        "keywords": ["natural light", "authentic", "soft", "organic", "window light"],
        "description_tr": "Doğal ışıkta, yumuşak gölgeler ve otantik atmosfer ile çekilmiş"
    },

    "outdoor": {
        "name": "Outdoor",
        "name_tr": "Dış Mekan",
        "tone": "fresh, natural, adventurous, real-world context",
        "lighting": "natural daylight, golden hour, outdoor conditions",
        "background": "nature, urban streets, outdoor environments",
        "props": "environmental elements, natural surroundings",
        "composition": "environmental context, real-world settings",
        "keywords": ["outdoor", "nature", "fresh", "environmental", "natural"],
        "description_tr": "Dış mekanda, doğal ortamda veya şehir sokakların da çekilmiş"
    },

    "macro_detail": {
        "name": "Macro Detail",
        "name_tr": "Makro Detay",
        "tone": "detailed, technical, quality-focused, intricate",
        "lighting": "focused lighting to highlight texture and detail",
        "background": "blurred or neutral to emphasize detail",
        "props": "none, focus on product detail",
        "composition": "extreme close-up, shallow depth of field, texture focus",
        "keywords": ["macro", "detail", "close-up", "texture", "intricate"],
        "description_tr": "Aşırı yakın çekim ile, ürünün detayları ve dokusunu vurgulayan"
    },

    "contextual": {
        "name": "Contextual",
        "name_tr": "Bağlamsal (Kullanımda)",
        "tone": "practical, relatable, usage-focused, real-life",
        "lighting": "natural or ambient lighting appropriate to context",
        "background": "relevant environment where product is used",
        "props": "contextual items showing product in use",
        "composition": "product in natural use scenario, environmental storytelling",
        "keywords": ["contextual", "in-use", "practical", "environment", "scenario"],
        "description_tr": "Ürünün kullanıldığı gerçek ortamda, kullanım senaryosu ile çekilmiş"
    },

    "monochrome": {
        "name": "Monochrome",
        "name_tr": "Siyah & Beyaz",
        "tone": "timeless, classic, elegant, artistic",
        "lighting": "emphasis on contrast, tonal range, shadows and highlights",
        "background": "any background, rendered in black and white",
        "props": "chosen for shape and contrast rather than color",
        "composition": "focus on form, texture, contrast, and composition",
        "keywords": ["monochrome", "black and white", "timeless", "contrast", "tonal"],
        "description_tr": "Siyah beyaz çekim ile, form ve kontrasta odaklanmış, zamansız bir estetik"
    },

    "seasonal": {
        "name": "Seasonal",
        "name_tr": "Mevsimsel",
        "tone": "timely, festive, seasonal relevance, trend-aligned",
        "lighting": "appropriate to season (warm for autumn, bright for summer)",
        "background": "seasonal elements (fall leaves, snow, flowers, beach)",
        "props": "season-specific items and decorations",
        "composition": "themed around current season or upcoming holiday",
        "keywords": ["seasonal", "holiday", "festive", "timely", "themed"],
        "description_tr": "Mevsime uygun dekorasyonlar ve temalar ile çekilmiş"
    },

    "geometric": {
        "name": "Geometric & Architectural",
        "name_tr": "Geometrik & Mimari",
        "tone": "structured, modern, architectural, precise",
        "lighting": "clean lighting, emphasis on lines and shapes",
        "background": "geometric patterns, architectural elements, clean lines",
        "props": "geometric shapes, architectural pieces",
        "composition": "strong lines, symmetry, geometric patterns, architectural framing",
        "keywords": ["geometric", "architectural", "structured", "lines", "modern"],
        "description_tr": "Geometrik şekiller ve mimari elementlerle, yapısal kompozisyonlar"
    },

    "texture_focus": {
        "name": "Texture Focus",
        "name_tr": "Doku Odaklı",
        "tone": "tactile, sensory, material-focused, quality emphasis",
        "lighting": "raking light to emphasize texture, side lighting",
        "background": "complementary textures or neutral to highlight product texture",
        "props": "textural elements that complement product material",
        "composition": "close-up or angled to showcase material and texture",
        "keywords": ["texture", "material", "tactile", "fabric", "surface"],
        "description_tr": "Ürünün dokusunu ve malzemesini öne çıkaran, dokunsal detaylar"
    },

    "transparent": {
        "name": "Transparent & Reflective",
        "name_tr": "Şeffaf & Yansıtıcı",
        "tone": "technical, clean, premium, glass-like",
        "lighting": "controlled lighting to manage reflections, backlight for transparency",
        "background": "clean backgrounds that don't interfere with reflections",
        "props": "reflective surfaces, glass elements",
        "composition": "careful angle management for reflections, showcase transparency",
        "keywords": ["transparent", "glass", "reflective", "crystal", "clear"],
        "description_tr": "Şeffaf ve yansıtıcı ürünler için özel aydınlatma teknikleri ile çekilmiş"
    }
}

PLATFORM_TEMPLATES = {
    "instagram": {
        "name": "Instagram",
        "aspect_ratio": "1:1 (square) or 9:16 (reels/stories)",
        "style_focus": "eye-catching, bold colors, clean composition, trendy aesthetics",
        "tips": "Leave space for text overlay, use trending color palettes, ensure mobile-friendly",
        "tips_tr": "Yazı eklemek için alan bırak, trend renk paletleri kullan, mobil uyumlu olsun"
    },

    "ecommerce": {
        "name": "E-ticaret",
        "aspect_ratio": "4:5 or 1:1",
        "style_focus": "white/light background, multiple angles, detail shots, clear product view",
        "tips": "Show product clearly from all angles, include size reference, consistent lighting",
        "tips_tr": "Ürünü her açıdan net göster, ölçü referansı ekle, tutarlı aydınlatma kullan"
    },

    "pinterest": {
        "name": "Pinterest",
        "aspect_ratio": "2:3 (vertical)",
        "style_focus": "inspirational, mood board style, lifestyle context, vertical composition",
        "tips": "Use text overlays with key info, create desire, show usage scenarios",
        "tips_tr": "Ana bilgileri metin olarak ekle, ilham verici olsun, kullanım senaryoları göster"
    },

    "catalog": {
        "name": "Katalog",
        "aspect_ratio": "1:1",
        "style_focus": "professional, consistent lighting, clean background, standard angles",
        "tips": "Multiple products same style, consistent color palette, uniform composition",
        "tips_tr": "Tüm ürünler aynı tarzda, tutarlı renk paleti, standart kompozisyon"
    }
}

CATEGORY_GUIDELINES = {
    "fashion": {
        "focus": "texture, fit, movement, drape",
        "common_settings": ["studio white background", "outdoor lifestyle", "editorial dark mood"],
        "must_show": ["fabric detail and texture", "how it fits on body", "styling options"],
        "avoid": "overly busy backgrounds that distract from clothing"
    },

    "food": {
        "focus": "texture, freshness, appetite appeal, ingredients",
        "common_settings": ["rustic wood table", "bright modern kitchen", "outdoor picnic"],
        "must_show": ["steam or freshness indicators", "key ingredients", "portion size"],
        "avoid": "cold/unappetizing lighting, artificial-looking food"
    },

    "tech": {
        "focus": "design details, features, scale, interfaces",
        "common_settings": ["minimal clean background", "desk setup", "hands-on usage demo"],
        "must_show": ["ports and buttons", "size comparison object", "screen/display quality"],
        "avoid": "cluttered backgrounds, poor lighting on screens"
    },

    "home_decor": {
        "focus": "ambiance, texture, how it fits in space",
        "common_settings": ["styled room setting", "close-up material details", "lifestyle context"],
        "must_show": ["how it looks in a room", "material and texture closeup", "available colors"],
        "avoid": "poor room styling, mismatched decor"
    },

    "accessories": {
        "focus": "details, craftsmanship, how to use/wear",
        "common_settings": ["flatlay composition", "on model/mannequin", "lifestyle in use"],
        "must_show": ["craftsmanship details", "size scale", "usage demonstration"],
        "avoid": "unclear product details, poor focus"
    },

    "beauty": {
        "focus": "texture, color accuracy, application, results",
        "common_settings": ["clean white background", "lifestyle application", "before/after"],
        "must_show": ["true color/texture", "application method", "results on skin"],
        "avoid": "color inaccuracy, poor skin tone representation"
    }
}


def get_style_template(style_key: str) -> dict:
    """Get style template by key."""
    return STYLE_TEMPLATES.get(style_key, STYLE_TEMPLATES["minimal"])


def get_platform_template(platform_key: str) -> dict:
    """Get platform template by key."""
    return PLATFORM_TEMPLATES.get(platform_key, PLATFORM_TEMPLATES["ecommerce"])


def get_category_guidelines(category: str) -> dict:
    """Get category guidelines. Returns default if category not found."""
    # Simple category matching
    category_lower = category.lower()

    for key, guidelines in CATEGORY_GUIDELINES.items():
        if key in category_lower:
            return guidelines

    # Default guidelines
    return {
        "focus": "product details, quality, usability",
        "common_settings": ["clean background", "lifestyle context", "detail shots"],
        "must_show": ["product details", "scale/size", "key features"],
        "avoid": "poor lighting, cluttered backgrounds"
    }


def get_all_styles() -> list[dict]:
    """Get all available styles for UI selection."""
    return [
        {
            "key": key,
            "name": template["name"],
            "name_tr": template["name_tr"],
            "description_tr": template["description_tr"]
        }
        for key, template in STYLE_TEMPLATES.items()
    ]
