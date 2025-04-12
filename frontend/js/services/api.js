// API Service using Axios

// Base URL for API calls
const API_BASE_URL = 'http://localhost:3000/api';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    timeout: 10000 // 10 seconds timeout
});

// API service object
const apiService = {
    // Send message to the chatbot
    sendMessage: async (message) => {
        try {
            const response = await apiClient.post('/chat', { message });
            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    },

    // Get chat history
    getChatHistory: async () => {
        try {
            const response = await apiClient.get('/history');
            return response.data;
        } catch (error) {
            console.error('Error fetching chat history:', error);
            throw error;
        }
    },

    // Create a new chat session
    createNewChat: async () => {
        try {
            const response = await apiClient.post('/chat/new');
            return response.data;
        } catch (error) {
            console.error('Error creating new chat:', error);
            throw error;
        }
    }
};
