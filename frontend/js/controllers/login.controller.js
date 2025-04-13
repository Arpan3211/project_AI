// Login Controller
// Handles login page functionality

import { authApi } from '../services/api.service.js';
import { validateEmail } from '../utils/validation.js';

class LoginController {
    constructor() {
        // DOM Elements
        this.loginForm = document.getElementById('login-form');
        this.emailInput = document.getElementById('login-email');
        this.passwordInput = document.getElementById('login-password');

        // Create error message element if it doesn't exist
        this.errorMessage = document.getElementById('error-message');
        if (!this.errorMessage) {
            this.errorMessage = document.createElement('div');
            this.errorMessage.id = 'error-message';
            this.errorMessage.className = 'error-message';
            this.errorMessage.style.display = 'none';

            // Insert after form heading
            const formHeading = document.querySelector('.auth-header');
            if (formHeading) {
                formHeading.parentNode.insertBefore(this.errorMessage, formHeading.nextSibling);
            } else if (this.loginForm) {
                this.loginForm.parentNode.insertBefore(this.errorMessage, this.loginForm);
            }
        }

        // Bind methods to this instance
        this.init = this.init.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
    }

    // Initialize the login page
    init() {
        // Check if user is already logged in
        const token = localStorage.getItem('token');
        if (token) {
            window.location.href = 'chat.html';
            return;
        }

        // Add event listeners
        if (this.loginForm) {
            this.loginForm.addEventListener('submit', this.handleLogin);
        } else {
            console.error('Login form not found');
        }
    }

    // Handle login form submission
    async handleLogin(e) {
        e.preventDefault();

        // Check if inputs exist
        if (!this.emailInput || !this.passwordInput) {
            this.showError('Form inputs not found');
            console.error('Email or password input not found');
            return;
        }

        const email = this.emailInput.value.trim();
        const password = this.passwordInput.value.trim();

        // Validate inputs
        if (!email || !password) {
            this.showError('Please enter both email and password');
            return;
        }

        if (!validateEmail(email)) {
            this.showError('Please enter a valid email address');
            return;
        }

        try {
            debugger
            // Show loading state
            this.loginForm.classList.add('loading');

            // Call login API
            const data = await authApi.login(email, password);

            // Save token and user data
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            // Redirect to chat page
            window.location.href = 'chat.html';
        } catch (error) {
            console.error('Login error:', error);
            this.showError(error.message || 'Login failed. Please check your credentials.');
        } finally {
            // Hide loading state
            this.loginForm.classList.remove('loading');
        }
    }

    // No need for password strength meter on login page

    // Show error message
    showError(message) {
        if (!this.errorMessage) {
            console.error('Error message element not found');
            alert(message); // Fallback to alert if error element doesn't exist
            return;
        }

        this.errorMessage.textContent = message;
        this.errorMessage.style.display = 'block';

        // Hide error after 5 seconds
        setTimeout(() => {
            if (this.errorMessage) {
                this.errorMessage.style.display = 'none';
            }
        }, 5000);
    }
}

// Initialize controller when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const loginController = new LoginController();
    loginController.init();
});

export default LoginController;
