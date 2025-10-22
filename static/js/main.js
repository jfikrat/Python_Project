/**
 * Main Application
 * Handles initialization, event listeners, and application state
 */

// Application State
window.appState = {
    currentProduct: null,
    selectedIdea: null,
    detectionData: null,
    sessionId: null
};

// DOM Elements
const elements = {
    uploadArea: null,
    fileInput: null,
    imagePreview: null,
    previewImg: null,
    loading: null,
    errorMessage: null,
    detectionResult: null,
    productName: null,
    productCategory: null,
    productConfidence: null,
    attributesContainer: null,
    ideasGrid: null,
    countSelection: null,
    shotCount: null,
    promptsSection: null,
    promptsContainer: null
};

/**
 * Initialize the application
 */
function initApp() {
    // Get DOM elements
    elements.uploadArea = document.getElementById('uploadArea');
    elements.fileInput = document.getElementById('fileInput');
    elements.imagePreview = document.getElementById('imagePreview');
    elements.previewImg = document.getElementById('previewImg');
    elements.loading = document.getElementById('loading');
    elements.errorMessage = document.getElementById('errorMessage');
    elements.detectionResult = document.getElementById('detectionResult');
    elements.productName = document.getElementById('productName');
    elements.productCategory = document.getElementById('productCategory');
    elements.productConfidence = document.getElementById('productConfidence');
    elements.attributesContainer = document.getElementById('attributesContainer');
    elements.ideasGrid = document.getElementById('ideasGrid');
    elements.countSelection = document.getElementById('countSelection');
    elements.shotCount = document.getElementById('shotCount');
    elements.promptsSection = document.getElementById('promptsSection');
    elements.promptsContainer = document.getElementById('promptsContainer');

    // Initialize UI elements in ui.js
    initUIElements(elements);

    // Setup event listeners
    setupEventListeners();
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // File upload
    elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);
}

/**
 * Handle file selection from input
 */
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

/**
 * Handle drag over event
 */
function handleDragOver(e) {
    e.preventDefault();
    elements.uploadArea.classList.add('dragover');
}

/**
 * Handle drag leave event
 */
function handleDragLeave() {
    elements.uploadArea.classList.remove('dragover');
}

/**
 * Handle drop event
 */
function handleDrop(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFile(file);
    } else {
        showError('Lütfen geçerli bir resim dosyası yükleyin!');
    }
}

/**
 * Handle file upload and detection
 */
async function handleFile(file) {
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        elements.previewImg.src = e.target.result;
        elements.imagePreview.classList.add('active');
    };
    reader.readAsDataURL(file);

    // Hide upload area, show loading
    elements.uploadArea.style.display = 'none';
    showLoading('AI ürünü analiz ediyor...');
    elements.errorMessage.classList.remove('active');

    try {
        const data = await detectProduct(file);
        window.appState.detectionData = data;
        window.appState.currentProduct = data.product;
        window.appState.sessionId = data.session_id;

        hideLoading();
        displayDetectionResult(data);
    } catch (error) {
        console.error('Detection error:', error);
        showError('Hata: ' + error.message);
        elements.uploadArea.style.display = 'block';
        hideLoading();
    }
}

/**
 * Select an idea card
 */
function selectIdea(idea, cardElement) {
    // Remove previous selection
    document.querySelectorAll('.idea-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Select new idea
    cardElement.classList.add('selected');
    window.appState.selectedIdea = idea;

    // Show count selection
    elements.countSelection.classList.add('active');
}

/**
 * Generate prompts for selected idea
 */
async function generatePromptsAction() {
    if (!window.appState.selectedIdea) {
        showError('Lütfen bir fikir seçin!');
        return;
    }

    const count = parseInt(elements.shotCount.value);
    if (count < 1 || count > 12) {
        showError('Lütfen 1-12 arası bir sayı girin!');
        return;
    }

    showLoading('AI promptları oluşturuyor...');
    elements.errorMessage.classList.remove('active');

    try {
        const data = await generatePrompts(
            window.appState.currentProduct,
            window.appState.selectedIdea.id,
            count,
            window.appState.sessionId
        );

        hideLoading();
        displayPrompts(data.shots);
    } catch (error) {
        console.error('Prompt generation error:', error);
        showError('Hata: ' + error.message);
        hideLoading();
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
