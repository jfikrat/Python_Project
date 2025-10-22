/**
 * UI Service
 * Handles all UI updates and rendering
 */

// DOM Elements (will be initialized in main.js)
let uiElements = {};

/**
 * Initialize UI elements
 * @param {Object} els - Object containing DOM element references
 */
function initUIElements(els) {
    uiElements = els;
}

/**
 * Display product detection result with ideas
 * @param {Object} data - Detection result from API
 */
function displayDetectionResult(data) {
    // Display product info
    uiElements.productName.textContent = data.product;
    uiElements.productCategory.textContent = data.category;
    uiElements.productConfidence.textContent = data.confidence;

    // Display attributes (XSS-safe)
    uiElements.attributesContainer.textContent = '';
    const strong = document.createElement('strong');
    strong.textContent = 'Özellikler: ';
    uiElements.attributesContainer.appendChild(strong);
    uiElements.attributesContainer.appendChild(document.createTextNode(data.attributes.join(', ')));

    // Display ideas
    uiElements.ideasGrid.innerHTML = '';
    data.ideas.forEach((idea) => {
        const ideaCard = createIdeaCard(idea);
        uiElements.ideasGrid.appendChild(ideaCard);
    });

    // Show detection result section
    uiElements.detectionResult.classList.add('active');
}

/**
 * Create an idea card element
 * @param {Object} idea - Idea data
 * @returns {HTMLElement} Idea card element
 */
function createIdeaCard(idea) {
    const card = document.createElement('div');
    card.className = 'idea-card';
    card.onclick = () => selectIdea(idea, card);

    // Create elements safely (XSS-protected)
    const ideaId = document.createElement('div');
    ideaId.className = 'idea-id';
    ideaId.textContent = idea.id;

    const title = document.createElement('h4');
    title.textContent = idea.title;

    const summaryP = document.createElement('p');
    const summaryStrong = document.createElement('strong');
    summaryStrong.textContent = 'Açıklama: ';
    summaryP.appendChild(summaryStrong);
    summaryP.appendChild(document.createTextNode(idea.summary));

    const whyP = document.createElement('p');
    const whyStrong = document.createElement('strong');
    whyStrong.textContent = 'Neden işe yarar: ';
    whyP.appendChild(whyStrong);
    whyP.appendChild(document.createTextNode(idea.why_it_works));

    const keywordsDiv = document.createElement('div');
    keywordsDiv.className = 'idea-keywords';
    idea.shot_keywords.forEach(keyword => {
        const span = document.createElement('span');
        span.className = 'keyword';
        span.textContent = keyword;
        keywordsDiv.appendChild(span);
    });

    // Append all elements
    card.appendChild(ideaId);
    card.appendChild(title);
    card.appendChild(summaryP);
    card.appendChild(whyP);
    card.appendChild(keywordsDiv);

    return card;
}

/**
 * Display generated prompts (NEW FORMAT)
 * @param {Array} shots - Array of prompt objects
 */
function displayPrompts(shots) {
    uiElements.promptsContainer.innerHTML = '';

    shots.forEach(shot => {
        const promptCard = createPromptCard(shot);
        uiElements.promptsContainer.appendChild(promptCard);
    });

    // Hide previous sections, show prompts
    uiElements.detectionResult.classList.remove('active');
    uiElements.promptsSection.classList.add('active');

    // Scroll to prompts
    uiElements.promptsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Create a prompt card element (NEW FORMAT)
 * @param {Object} shot - Prompt data with index, title, style_description, gen_prompt
 * @returns {HTMLElement} Prompt card element
 */
function createPromptCard(shot) {
    const card = document.createElement('div');
    card.className = 'prompt-card';

    const promptId = `prompt-${shot.index}`;

    // Create header (XSS-protected)
    const header = document.createElement('div');
    header.className = 'prompt-header';

    const number = document.createElement('div');
    number.className = 'prompt-number';
    number.textContent = shot.index;

    const title = document.createElement('div');
    title.className = 'prompt-title';
    title.textContent = shot.title;

    header.appendChild(number);
    header.appendChild(title);

    // Create style description (XSS-protected)
    const styleDesc = document.createElement('div');
    styleDesc.className = 'style-description';

    const styleLabel = document.createElement('div');
    styleLabel.className = 'style-label';
    styleLabel.textContent = 'Stil Açıklaması';

    const styleValue = document.createElement('div');
    styleValue.className = 'style-value';
    styleValue.textContent = shot.style_description;

    styleDesc.appendChild(styleLabel);
    styleDesc.appendChild(styleValue);

    // Create prompt display (XSS-protected)
    const promptDisplay = document.createElement('div');
    promptDisplay.className = 'prompt-display';

    const promptBox = document.createElement('div');
    promptBox.className = 'prompt-box';
    promptBox.id = promptId;
    promptBox.textContent = shot.gen_prompt;

    const promptActions = document.createElement('div');
    promptActions.className = 'prompt-actions';

    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = '📋 Kopyala';
    copyBtn.onclick = () => copyPrompt(promptId, copyBtn);

    promptActions.appendChild(copyBtn);
    promptDisplay.appendChild(promptBox);
    promptDisplay.appendChild(promptActions);

    // Append all to card
    card.appendChild(header);
    card.appendChild(styleDesc);
    card.appendChild(promptDisplay);

    return card;
}

/**
 * Copy prompt to clipboard
 * @param {string} promptId - ID of the prompt element
 * @param {HTMLElement} button - Copy button element
 */
function copyPrompt(promptId, button) {
    const promptText = document.getElementById(promptId).textContent;

    navigator.clipboard.writeText(promptText).then(() => {
        // Visual feedback
        button.textContent = '✓ Kopyalandı!';
        button.classList.add('copied');

        // Reset after 2 seconds
        setTimeout(() => {
            button.textContent = '📋 Kopyala';
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        showError('Kopyalama başarısız oldu!');
    });
}

/**
 * Show loading state
 * @param {string} message - Loading message
 */
function showLoading(message = 'AI ürünü analiz ediyor...') {
    uiElements.loading.querySelector('p').textContent = message;
    uiElements.loading.classList.add('active');
}

/**
 * Hide loading state
 */
function hideLoading() {
    uiElements.loading.classList.remove('active');
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    uiElements.errorMessage.textContent = message;
    uiElements.errorMessage.classList.add('active');

    setTimeout(() => {
        uiElements.errorMessage.classList.remove('active');
    }, 5000);
}

/**
 * Reset the entire application to initial state
 */
function resetApp() {
    // Reset state (handled in main.js)
    window.appState.currentProduct = null;
    window.appState.selectedIdea = null;
    window.appState.detectionData = null;

    // Reset UI
    uiElements.uploadArea.style.display = 'block';
    uiElements.imagePreview.classList.remove('active');
    uiElements.detectionResult.classList.remove('active');
    uiElements.countSelection.classList.remove('active');
    uiElements.promptsSection.classList.remove('active');
    uiElements.errorMessage.classList.remove('active');
    uiElements.fileInput.value = '';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
