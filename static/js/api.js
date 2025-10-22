/**
 * API Service
 * Handles all API communication with the backend
 */

// Dynamically determine API base URL from current origin
// Works in development (localhost:8000) and production
const API_BASE = window.location.origin;

/**
 * Detect product from uploaded image and get creative ideas
 * @param {File} file - The image file to upload
 * @param {string} style - Optional style preference (minimal, luxury, lifestyle, etc.)
 * @param {string} modelPreference - Optional model preference ('with_model' or 'without_model')
 * @param {string} aiModel - Optional AI model to use (gpt-4.1-mini, etc.)
 * @returns {Promise<Object>} Detection result with product info and ideas
 */
async function detectProduct(file, style = null, modelPreference = null, aiModel = null) {
    const formData = new FormData();
    formData.append('file', file);

    // Add parameters as query parameters if provided
    const url = new URL(`${API_BASE}/api/detect`);
    if (style) {
        url.searchParams.append('style', style);
    }
    if (modelPreference) {
        url.searchParams.append('model_preference', modelPreference);
    }
    if (aiModel) {
        url.searchParams.append('ai_model', aiModel);
    }

    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

/**
 * Generate image generation prompts based on selected idea
 * @param {string} product - Product name
 * @param {string} ideaId - Selected idea ID (e.g., "I1")
 * @param {number} count - Number of prompts to generate (1-12)
 * @param {string} sessionId - Session ID from detection response
 * @param {string} aiModel - Optional AI model to use
 * @returns {Promise<Object>} Response with generated prompts
 */
async function generatePrompts(product, ideaId, count, sessionId, aiModel = null) {
    const requestBody = {
        product: product,
        idea_id: ideaId,
        count: count,
        session_id: sessionId
    };

    if (aiModel) {
        requestBody.ai_model = aiModel;
    }

    const response = await fetch(`${API_BASE}/api/plan`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
async function checkHealth() {
    const response = await fetch(`${API_BASE}/api/health`);
    return await response.json();
}
