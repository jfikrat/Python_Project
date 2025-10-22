/**
 * Chat Service
 * Handles conversational UI and message management
 */

// Chat state
const chatState = {
    messages: [],
    isTyping: false,
    currentSession: null,
    uploadedImage: null,
    uploadedFile: null,
    selectedStyle: null,
    modelPreference: null,  // 'with_model' or 'without_model'
    aiModel: null,  // AI model to use (gpt-4.1-mini, etc.)
    waitingFor: null,  // Track what we're waiting for: 'ai_model', 'style', 'model', 'idea', 'prompt_count'
    pendingIdeaId: null  // Store idea ID when waiting for prompt count
};

// DOM elements
let chatElements = {};

/**
 * Initialize chat UI
 */
function initChat() {
    chatElements = {
        messagesContainer: document.getElementById('chatMessages'),
        inputField: document.getElementById('chatInput'),
        sendBtn: document.getElementById('chatSendBtn'),
        uploadBtn: document.getElementById('chatUploadBtn'),
        uploadInput: document.getElementById('chatUploadInput'),
        modelBtn: document.getElementById('chatModelBtn'),
        currentModelName: document.getElementById('currentModelName')
    };

    // Event listeners
    chatElements.sendBtn.addEventListener('click', handleSendMessage);
    chatElements.inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    chatElements.uploadBtn.addEventListener('click', () => chatElements.uploadInput.click());
    chatElements.uploadInput.addEventListener('change', handleImageUpload);
    chatElements.modelBtn.addEventListener('click', changeAIModel);

    // Ask for AI model selection first
    askAIModelSelection();
}

/**
 * Add a message to the chat
 */
function addMessage(content, type = 'ai', options = {}) {
    const message = {
        id: Date.now(),
        content,
        type,
        timestamp: new Date(),
        ...options
    };

    chatState.messages.push(message);
    renderMessage(message);
    scrollToBottom();

    return message;
}

/**
 * Add AI message with optional typewriter effect
 */
function addAIMessage(content, options = {}) {
    return addMessage(content, 'ai', { useTypewriter: true, ...options });
}

/**
 * Add user message
 */
function addUserMessage(content, options = {}) {
    return addMessage(content, 'user', options);
}

/**
 * Add thinking message (AI is processing)
 */
function addThinkingMessage(content = "Düşünüyorum...") {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message ai thinking-message';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar ai';
    avatar.textContent = '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble thinking';
    bubble.textContent = content;

    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        typingIndicator.appendChild(dot);
    }

    bubble.appendChild(typingIndicator);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    chatElements.messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    return messageDiv;
}

/**
 * Remove thinking message
 */
function removeThinkingMessage() {
    const thinkingMsg = chatElements.messagesContainer.querySelector('.thinking-message');
    if (thinkingMsg) {
        thinkingMsg.remove();
    }
}

/**
 * Render a message in the chat
 */
function renderMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${message.type}`;
    messageDiv.dataset.messageId = message.id;

    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${message.type}`;
    avatar.textContent = message.type === 'ai' ? '🤖' : '👤';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    // Handle different content types
    if (message.image) {
        const imgContainer = document.createElement('div');
        imgContainer.className = 'message-image';
        const img = document.createElement('img');
        img.src = message.image;
        img.alt = 'Uploaded image';
        imgContainer.appendChild(img);
        bubble.appendChild(imgContainer);
    }

    if (message.content) {
        const textNode = document.createElement('div');

        if (message.useTypewriter && message.type === 'ai') {
            typewriterEffect(textNode, message.content);
        } else {
            textNode.textContent = message.content;
        }

        bubble.appendChild(textNode);
    }

    // Add quick action buttons if provided
    if (message.actions) {
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'quick-actions';

        message.actions.forEach(action => {
            const btn = document.createElement('button');
            btn.className = 'quick-action-btn';
            btn.textContent = action.label;
            btn.onclick = () => action.callback(action.value);
            actionsDiv.appendChild(btn);
        });

        bubble.appendChild(actionsDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    chatElements.messagesContainer.appendChild(messageDiv);
}

/**
 * Typewriter effect for AI messages
 */
function typewriterEffect(element, text, speed = 30) {
    let index = 0;
    element.classList.add('typewriter');

    const cursor = document.createElement('span');
    cursor.className = 'typewriter-cursor';

    function type() {
        if (index < text.length) {
            element.textContent = text.substring(0, index + 1);
            element.appendChild(cursor);
            index++;
            setTimeout(type, speed);
        } else {
            cursor.remove();
            element.classList.remove('typewriter');
        }
    }

    type();
}

/**
 * Handle send message
 */
function handleSendMessage() {
    const text = chatElements.inputField.value.trim();
    if (!text) return;

    // Add user message
    addUserMessage(text);
    chatElements.inputField.value = '';

    // Process user input
    processUserInput(text);
}

/**
 * Handle image upload
 */
async function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file || !file.type.startsWith('image/')) {
        addAIMessage("⚠️ Lütfen geçerli bir resim dosyası yükleyin!");
        return;
    }

    // Read and display image
    const reader = new FileReader();
    reader.onload = (event) => {
        chatState.uploadedImage = event.target.result;
        chatState.uploadedFile = file;
        addUserMessage("", { image: event.target.result });

        // Ask for style preference first
        askStylePreference();
    };
    reader.readAsDataURL(file);

    // Clear input
    e.target.value = '';
}

/**
 * Ask user for AI model selection
 */
async function askAIModelSelection() {
    chatState.waitingFor = 'ai_model';
    addAIMessage("Merhaba! 👋 Ben senin AI çekim asistanınım.\n\nHangi AI modelini kullanmak istersin? 🤖", {
        actions: [
            {
                label: '⚡ GPT-4o Mini (ÖNERİLEN)',
                value: 'gpt-4o-mini',
                callback: (model) => selectAIModel(model),
                description: '✓ Güvenilir ve hızlı - 2024'
            },
            {
                label: '🔥 GPT-4.1 Mini',
                value: 'gpt-4.1-mini',
                callback: (model) => selectAIModel(model),
                description: '✓ Güçlü ve ekonomik - Nisan 2025'
            },
            {
                label: '🧪 GPT-5 Mini (DENEYSEL)',
                value: 'gpt-5-mini',
                callback: (model) => selectAIModel(model),
                description: '⚠ Henüz API\'de olmayabilir'
            },
            {
                label: '🧪 GPT-5 (DENEYSEL)',
                value: 'gpt-5',
                callback: (model) => selectAIModel(model),
                description: '⚠ En yeni model - API\'de olmayabilir'
            },
            {
                label: '🧪 GPT-5 Nano (DENEYSEL)',
                value: 'gpt-5-nano',
                callback: (model) => selectAIModel(model),
                description: '⚠ Henüz API\'de olmayabilir'
            },
            {
                label: '🧪 o4-mini (DENEYSEL)',
                value: 'o4-mini',
                callback: (model) => selectAIModel(model),
                description: '⚠ Akıl yürütme modeli - Deneysel'
            }
        ]
    });
}

/**
 * Handle AI model selection
 */
function selectAIModel(modelKey, showWelcome = true) {
    const modelNames = {
        'gpt-5': 'GPT-5',
        'gpt-5-mini': 'GPT-5 Mini',
        'gpt-5-nano': 'GPT-5 Nano',
        'o4-mini': 'o4-mini',
        'gpt-4.1': 'GPT-4.1',
        'gpt-4.1-mini': 'GPT-4.1 Mini',
        'gpt-4.1-nano': 'GPT-4.1 Nano',
        'gpt-4o-mini': 'GPT-4o Mini'
    };

    addUserMessage(`${modelNames[modelKey]} modelini seçtim`);
    chatState.aiModel = modelKey;
    chatState.waitingFor = null;

    // Update model button label
    updateModelButtonLabel(modelKey);

    // Welcome message after model selection (only on first selection)
    if (showWelcome) {
        setTimeout(() => {
            addAIMessage(`Harika! ${modelNames[modelKey]} ile çalışacağız. Hangi ürünü çekmek istiyorsun? Fotoğrafını yükleyerek başlayalım! 📸`);
        }, 500);
    } else {
        setTimeout(() => {
            addAIMessage(`Model değiştirildi: ${modelNames[modelKey]} 🔄`);
        }, 500);
    }
}

/**
 * Update model button label with current model name
 */
function updateModelButtonLabel(modelKey) {
    const shortNames = {
        'gpt-5': 'GPT-5',
        'gpt-5-mini': 'GPT-5 Mini',
        'gpt-5-nano': 'GPT-5 Nano',
        'o4-mini': 'o4-mini',
        'gpt-4.1': 'GPT-4.1',
        'gpt-4.1-mini': 'GPT-4.1 Mini',
        'gpt-4.1-nano': 'GPT-4.1 Nano',
        'gpt-4o-mini': 'GPT-4o Mini'
    };

    if (chatElements.currentModelName) {
        chatElements.currentModelName.textContent = shortNames[modelKey] || 'Model';
    }
}

/**
 * Change AI model (triggered by model button click)
 */
function changeAIModel() {
    chatState.waitingFor = 'ai_model_change';
    addAIMessage("Hangi AI modelini kullanmak istersin? 🤖", {
        actions: [
            {
                label: '⚡ GPT-4o Mini (ÖNERİLEN)',
                value: 'gpt-4o-mini',
                callback: (model) => selectAIModel(model, false),
                description: '✓ Güvenilir ve hızlı - 2024'
            },
            {
                label: '🔥 GPT-4.1 Mini',
                value: 'gpt-4.1-mini',
                callback: (model) => selectAIModel(model, false),
                description: '✓ Güçlü ve ekonomik - Nisan 2025'
            },
            {
                label: '🧪 GPT-5 Mini (DENEYSEL)',
                value: 'gpt-5-mini',
                callback: (model) => selectAIModel(model, false),
                description: '⚠ Henüz API\'de olmayabilir'
            },
            {
                label: '🧪 GPT-5 (DENEYSEL)',
                value: 'gpt-5',
                callback: (model) => selectAIModel(model, false),
                description: '⚠ En yeni model - API\'de olmayabilir'
            },
            {
                label: '🧪 GPT-5 Nano (DENEYSEL)',
                value: 'gpt-5-nano',
                callback: (model) => selectAIModel(model, false),
                description: '⚠ Henüz API\'de olmayabilir'
            },
            {
                label: '🧪 o4-mini (DENEYSEL)',
                value: 'o4-mini',
                callback: (model) => selectAIModel(model, false),
                description: '⚠ Akıl yürütme modeli - Deneysel'
            }
        ]
    });
}

/**
 * Ask user for style preference
 */
async function askStylePreference() {
    chatState.waitingFor = 'style';
    addAIMessage("Harika! Hangi tarzda çekim istersin? 🎨 (Scroll yaparak tüm stilleri görebilirsin)", {
        actions: [
            { label: '✨ Minimalist', value: 'minimal', callback: (style) => selectStyle(style) },
            { label: '💎 Lüks', value: 'luxury', callback: (style) => selectStyle(style) },
            { label: '🌿 Lifestyle', value: 'lifestyle', callback: (style) => selectStyle(style) },
            { label: '📸 Vintage', value: 'vintage', callback: (style) => selectStyle(style) },
            { label: '🎯 Cesur/Canlı', value: 'bold', callback: (style) => selectStyle(style) },
            { label: '🏭 Endüstriyel', value: 'industrial', callback: (style) => selectStyle(style) },
            { label: '🎨 Dekoratif', value: 'decorative', callback: (style) => selectStyle(style) },
            { label: '⚪ Beyaz Zemin', value: 'white_background', callback: (style) => selectStyle(style) },
            { label: '📐 Flatlay', value: 'flatlay', callback: (style) => selectStyle(style) },
            { label: '📰 Editorial', value: 'editorial', callback: (style) => selectStyle(style) },
            { label: '🎬 Stüdyo', value: 'studio_clean', callback: (style) => selectStyle(style) },
            { label: '🌑 Koyu/Dramatik', value: 'dark_moody', callback: (style) => selectStyle(style) },
            { label: '🎪 Renkli Pop', value: 'colorful_pop', callback: (style) => selectStyle(style) },
            { label: '☀️ Doğal Işık', value: 'natural_light', callback: (style) => selectStyle(style) },
            { label: '🌳 Dış Mekan', value: 'outdoor', callback: (style) => selectStyle(style) },
            { label: '🔍 Makro Detay', value: 'macro_detail', callback: (style) => selectStyle(style) },
            { label: '🏠 Bağlamsal', value: 'contextual', callback: (style) => selectStyle(style) },
            { label: '⬛ Siyah/Beyaz', value: 'monochrome', callback: (style) => selectStyle(style) },
            { label: '🎄 Mevsimsel', value: 'seasonal', callback: (style) => selectStyle(style) },
            { label: '📐 Geometrik', value: 'geometric', callback: (style) => selectStyle(style) },
            { label: '🧵 Doku Odaklı', value: 'texture_focus', callback: (style) => selectStyle(style) },
            { label: '💎 Şeffaf/Cam', value: 'transparent', callback: (style) => selectStyle(style) }
        ]
    });
}

/**
 * Handle style selection
 */
function selectStyle(styleKey) {
    const styleNames = {
        'minimal': 'Minimalist & Modern',
        'luxury': 'Lüks & Premium',
        'lifestyle': 'Doğal & Lifestyle',
        'vintage': 'Vintage & Retro',
        'bold': 'Cesur & Canlı',
        'industrial': 'Endüstriyel & Kentsel',
        'decorative': 'Dekoratif & Sanatsal',
        'white_background': 'Beyaz Arka Plan',
        'flatlay': 'Yukarıdan Düzenleme',
        'editorial': 'Editorial (Dergi Tarzı)',
        'studio_clean': 'Temiz Stüdyo',
        'dark_moody': 'Koyu & Dramatik',
        'colorful_pop': 'Renkli & Pop',
        'natural_light': 'Doğal Işık',
        'outdoor': 'Dış Mekan',
        'macro_detail': 'Makro Detay',
        'contextual': 'Bağlamsal (Kullanımda)',
        'monochrome': 'Siyah & Beyaz',
        'seasonal': 'Mevsimsel',
        'geometric': 'Geometrik & Mimari',
        'texture_focus': 'Doku Odaklı',
        'transparent': 'Şeffaf & Yansıtıcı'
    };

    addUserMessage(`${styleNames[styleKey]} tarzını seçtim`);
    chatState.selectedStyle = styleKey;
    chatState.waitingFor = null;  // Clear waiting state

    // Ask for model preference next
    setTimeout(() => {
        askModelPreference();
    }, 500);
}

/**
 * Ask user for model preference
 */
async function askModelPreference() {
    chatState.waitingFor = 'model';
    addAIMessage("Çekimde model olsun mu? 👤", {
        actions: [
            { label: '👤 Modelli Çekim', value: 'with_model', callback: (pref) => selectModelPreference(pref) },
            { label: '📦 Sadece Ürün', value: 'without_model', callback: (pref) => selectModelPreference(pref) }
        ]
    });
}

/**
 * Handle model preference selection
 */
function selectModelPreference(preference) {
    const preferenceNames = {
        'with_model': 'Modelli çekim',
        'without_model': 'Sadece ürün odaklı çekim'
    };

    addUserMessage(`${preferenceNames[preference]} istiyorum`);
    chatState.modelPreference = preference;
    chatState.waitingFor = null;  // Clear waiting state

    // Now analyze with selected style and model preference
    analyzeProduct(chatState.uploadedFile, chatState.selectedStyle, chatState.modelPreference);
}

/**
 * Process user text input
 */
async function processUserInput(text) {
    // Check if we're waiting for specific input
    if (chatState.waitingFor === 'prompt_count') {
        // Try to parse as number
        const count = parseInt(text.trim());
        if (!isNaN(count) && count >= 1 && count <= 12) {
            // Valid number, proceed with prompt generation
            if (chatState.pendingIdeaId) {
                handleGeneratePrompts(chatState.pendingIdeaId, count);
                return;
            }
        } else {
            addAIMessage("Lütfen 1 ile 12 arasında bir sayı girin veya yukarıdaki butonlardan birini seçin. 🔢");
            return;
        }
    }

    // Simple intent detection
    const lowerText = text.toLowerCase();

    if (lowerText.includes('merhaba') || lowerText.includes('selam')) {
        addAIMessage("Merhaba! 😊 Hangi ürünü çekmek istiyorsun?");
    } else if (lowerText.includes('yardım') || lowerText.includes('help')) {
        addAIMessage("Tabii! Şu adımları takip edebiliriz:\n\n1️⃣ Ürün fotoğrafını yükle\n2️⃣ AI çekim fikirlerini gör\n3️⃣ Beğendiğin fikri seç\n4️⃣ AI görsel promptlarını al\n\nHazırsan, fotoğrafını yükle! 📸");
    } else {
        addAIMessage("Anladım! Ürünün fotoğrafını yüklemek ister misin? 📸");
    }
}

/**
 * Analyze uploaded product image
 */
async function analyzeProduct(file, style = null, modelPreference = null) {
    const thinkingMsg = addThinkingMessage("Fotoğrafı inceliyorum...");

    try {
        // Call API with optional style, model preference, and AI model
        const data = await detectProduct(file, style, modelPreference, chatState.aiModel);

        // Remove thinking indicator
        removeThinkingMessage();

        // Store session
        chatState.currentSession = {
            product: data.product,
            sessionId: data.session_id,
            ideas: data.ideas
        };

        // Build description for what was requested
        const styleNote = style ? ` ${chatState.selectedStyle} stilinde` : '';
        const modelNote = modelPreference === 'with_model' ? ' modelli' : '';

        addAIMessage(`Harika! ${data.product} tespit ettim! ✅\n\n📦 Kategori: ${data.category}\n🎯 Güven: %${data.confidence}`);

        setTimeout(() => {
            chatState.waitingFor = 'idea';  // Set state to waiting for idea selection
            addAIMessage(`${data.ideas.length} farklı${styleNote}${modelNote} çekim fikri hazırladım. Hangi fikri beğenirsin?`, {
                actions: data.ideas.map((idea, index) => ({
                    label: `${index + 1}. ${idea.title}`,
                    value: idea.id,
                    callback: (ideaId) => selectIdea(ideaId)
                }))
            });
        }, 800);

    } catch (error) {
        removeThinkingMessage();
        addAIMessage(`❌ Bir hata oluştu: ${error.message}\n\nTekrar denemek ister misin?`);
    }
}

/**
 * Handle idea selection
 */
function selectIdea(ideaId) {
    const idea = chatState.currentSession.ideas.find(i => i.id === ideaId);
    if (!idea) return;

    addUserMessage(`${idea.title} fikrini seçtim`);
    chatState.waitingFor = null;  // Clear previous waiting state

    // Show idea details
    setTimeout(() => {
        addAIMessage(`Mükemmel seçim! "${idea.title}" 🎨\n\n${idea.summary}\n\n💡 Neden işe yarar: ${idea.why_it_works}`);

        setTimeout(() => {
            chatState.waitingFor = 'prompt_count';  // Set state to waiting for prompt count
            chatState.pendingIdeaId = ideaId;  // Store idea ID for later use
            addAIMessage("Kaç tane görsel promptu oluşturayım? (1-12)", {
                actions: [
                    { label: '3 prompt', value: 3, callback: (count) => handleGeneratePrompts(ideaId, count) },
                    { label: '5 prompt', value: 5, callback: (count) => handleGeneratePrompts(ideaId, count) },
                    { label: '10 prompt', value: 10, callback: (count) => handleGeneratePrompts(ideaId, count) }
                ]
            });
        }, 800);
    }, 500);
}

/**
 * Generate prompts for selected idea
 */
async function handleGeneratePrompts(ideaId, count) {
    addUserMessage(`${count} prompt oluştur`);
    chatState.waitingFor = null;  // Clear waiting state
    chatState.pendingIdeaId = null;  // Clear pending idea

    const thinkingMsg = addThinkingMessage(`${count} adet görsel promptu oluşturuyorum...`);

    try {
        const data = await generatePrompts(
            chatState.currentSession.product,
            ideaId,
            count,
            chatState.currentSession.sessionId,
            chatState.aiModel
        );

        removeThinkingMessage();

        // Display prompts with click-to-copy functionality
        data.shots.forEach((shot, index) => {
            setTimeout(() => {
                addClickablePromptMessage(shot, index);
            }, index * 600);
        });

        // Ask for next action
        setTimeout(() => {
            addAIMessage("Başka bir şey yapabilir miyim? 😊", {
                actions: [
                    { label: '🔄 Yeni ürün', value: 'reset', callback: () => resetChat() },
                    { label: '🎨 Farklı fikir', value: 'ideas', callback: () => showIdeas() }
                ]
            });
        }, data.shots.length * 600 + 800);

    } catch (error) {
        removeThinkingMessage();
        addAIMessage(`❌ Promptlar oluşturulurken hata: ${error.message}`);
    }
}

/**
 * Add a clickable prompt message with click-to-copy
 */
function addClickablePromptMessage(shot, index) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    // Create title
    const title = document.createElement('div');
    title.className = 'prompt-title';
    title.textContent = `📸 ${shot.title}`;

    // Create style description
    const styleDesc = document.createElement('div');
    styleDesc.className = 'prompt-style';
    styleDesc.textContent = `🎨 ${shot.style_description}`;

    // Create prompt container (clickable)
    const promptContainer = document.createElement('div');
    promptContainer.className = 'prompt-clickable';
    promptContainer.setAttribute('title', 'Kopyalamak için tıkla');

    const promptLabel = document.createElement('div');
    promptLabel.className = 'prompt-label';
    promptLabel.textContent = '💬 Prompt (tıklayarak kopyala):';

    const promptText = document.createElement('div');
    promptText.className = 'prompt-text';
    promptText.textContent = shot.gen_prompt;

    promptContainer.appendChild(promptLabel);
    promptContainer.appendChild(promptText);

    // Add click handler to copy
    promptContainer.addEventListener('click', () => {
        navigator.clipboard.writeText(shot.gen_prompt).then(() => {
            showToast(`✅ Prompt ${index + 1} kopyalandı!`);
            promptContainer.classList.add('copied');
            setTimeout(() => {
                promptContainer.classList.remove('copied');
            }, 2000);
        });
    });

    bubble.appendChild(title);
    bubble.appendChild(styleDesc);
    bubble.appendChild(promptContainer);
    messageDiv.appendChild(bubble);

    chatElements.messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Show toast notification
 */
function showToast(message) {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text, successMessage) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(successMessage || "✅ Kopyalandı!");
    });
}

/**
 * Show ideas again
 */
function showIdeas() {
    if (!chatState.currentSession || !chatState.currentSession.ideas) return;

    chatState.waitingFor = 'idea';  // Set state to waiting for idea selection
    chatState.pendingIdeaId = null;  // Clear pending idea
    addAIMessage("İşte tekrar çekim fikirleri:", {
        actions: chatState.currentSession.ideas.map((idea, index) => ({
            label: `${index + 1}. ${idea.title}`,
            value: idea.id,
            callback: (ideaId) => selectIdea(ideaId)
        }))
    });
}

/**
 * Reset chat for new product
 */
function resetChat() {
    chatElements.messagesContainer.innerHTML = '';
    chatState.messages = [];
    chatState.currentSession = null;
    chatState.uploadedImage = null;
    chatState.uploadedFile = null;
    chatState.selectedStyle = null;
    chatState.modelPreference = null;
    // Keep aiModel - user doesn't need to reselect it
    chatState.waitingFor = null;
    chatState.pendingIdeaId = null;

    addAIMessage("Tamam! Yeni bir ürün için hazırım. Fotoğrafını yükle! 📸");
}

/**
 * Scroll to bottom of chat
 */
function scrollToBottom() {
    chatElements.messagesContainer.scrollTop = chatElements.messagesContainer.scrollHeight;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChat);
} else {
    initChat();
}
