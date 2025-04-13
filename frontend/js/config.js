// Configuration file to load environment variables
// This file centralizes all configuration settings for the frontend

// Load environment variables from .env file
// In a real production environment, you would use a proper env loader like dotenv
// For this simple example, we'll define the variables directly

// API URL for backend requests
export const API_URL = 'http://localhost:8000/api';

// Add other configuration variables here as needed
export const APP_NAME = 'AI Chat Assistant';
export const APP_VERSION = '1.0.0';

// Export default config object
export default {
    API_URL,
    APP_NAME,
    APP_VERSION
};
