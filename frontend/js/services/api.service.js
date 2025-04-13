// Centralized API Service
// All API calls should be made through this service

// Import config
import { API_URL } from '../config.js';

/**
 * Base API class with common methods for all API calls
 */
class ApiService {
    /**
     * Make a GET request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Additional fetch options
     * @returns {Promise} - Response data
     */
    async get(endpoint, options = {}) {
        const token = localStorage.getItem('token');

        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            },
            mode: 'cors',
            credentials: 'same-origin'
        };

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...defaultOptions,
            ...options
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API error: ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Make a POST request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body data
     * @param {Object} options - Additional fetch options
     * @returns {Promise} - Response data
     */
    async post(endpoint, data = {}, options = {}) {
        const token = localStorage.getItem('token');

        const defaultOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            },
            body: JSON.stringify(data),
            mode: 'cors',
            credentials: 'same-origin'
        };

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...defaultOptions,
            ...options
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API error: ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Make a PUT request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body data
     * @param {Object} options - Additional fetch options
     * @returns {Promise} - Response data
     */
    async put(endpoint, data = {}, options = {}) {
        const token = localStorage.getItem('token');

        const defaultOptions = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            },
            body: JSON.stringify(data),
            mode: 'cors',
            credentials: 'same-origin'
        };

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...defaultOptions,
            ...options
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API error: ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Make a DELETE request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Additional fetch options
     * @returns {Promise} - Response data
     */
    async delete(endpoint, options = {}) {
        const token = localStorage.getItem('token');

        const defaultOptions = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            },
            mode: 'cors',
            credentials: 'same-origin'
        };

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...defaultOptions,
            ...options
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API error: ${response.status}`);
        }

        return await response.json();
    }
}

// Create API service instance
const apiService = new ApiService();

/**
 * Auth API methods
 */
export const authApi = {
    /**
     * Register a new user
     * @param {Object} userData - User registration data
     * @returns {Promise} - User data
     */
    register: async (userData) => {
        return await apiService.post('/auth/register', userData);
    },

    /**
     * Login user
     * @param {string} email - User email
     * @param {string} password - User password
     * @returns {Promise} - Auth token and user data
     */
    login: async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData,
            mode: 'cors',
            credentials: 'same-origin'
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Login failed');
        }

        return await response.json();
    },

    /**
     * Get current user profile
     * @returns {Promise} - User profile data
     */
    getProfile: async () => {
        return await apiService.get('/auth/me');
    },

    /**
     * Logout user
     * @returns {Promise} - Logout confirmation
     */
    logout: async () => {
        try {
            await apiService.post('/auth/logout');
        } catch (error) {
            console.error('Error during logout:', error);
        } finally {
            // Clear auth data regardless of API success
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        }
        return { success: true };
    }
};

/**
 * Chat API methods
 */
export const chatApi = {
    /**
     * Get all conversations
     * @returns {Promise} - List of conversations
     */
    getConversations: async () => {
        return await apiService.get('/conversations');
    },

    /**
     * Get a specific conversation with messages
     * @param {number} conversationId - Conversation ID
     * @returns {Promise} - Conversation data with messages
     */
    getConversation: async (conversationId) => {
        return await apiService.get(`/conversations/${conversationId}`);
    },

    /**
     * Create a new conversation
     * @param {string} title - Conversation title
     * @returns {Promise} - New conversation data
     */
    createConversation: async (title = 'New Conversation') => {
        return await apiService.post('/conversations', { title });
    },

    /**
     * Send a message and get AI response
     * @param {string} message - User message
     * @param {number|null} conversationId - Conversation ID (optional)
     * @returns {Promise} - Message response data
     */
    sendMessage: async (message, conversationId = null) => {
        const payload = {
            role: 'user',
            content: message
        };

        if (conversationId) {
            payload.conversation_id = conversationId;
        }

        return await apiService.post('/chat', payload);
    },

    /**
     * Delete a conversation
     * @param {number} conversationId - Conversation ID
     * @returns {Promise} - Delete confirmation
     */
    deleteConversation: async (conversationId) => {
        return await apiService.delete(`/conversations/${conversationId}`);
    },

    /**
     * Update conversation title
     * @param {number} conversationId - Conversation ID
     * @param {string} title - New title
     * @returns {Promise} - Updated conversation data
     */
    updateConversationTitle: async (conversationId, title) => {
        return await apiService.put(`/conversations/${conversationId}?title=${encodeURIComponent(title)}`);
    }
};
