// Register Controller
// Handles registration page functionality

import { authApi } from '../services/api.service.js';
import { validateEmail, validatePassword } from '../utils/validation.js';

class RegisterController {
    constructor() {
        // DOM Elements
        this.registerForm = document.getElementById('register-form');
        this.nameInput = document.getElementById('register-name');
        this.emailInput = document.getElementById('register-email');
        this.passwordInput = document.getElementById('register-password');
        this.confirmPasswordInput = document.getElementById('register-confirm-password');

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
            } else if (this.registerForm) {
                this.registerForm.parentNode.insertBefore(this.errorMessage, this.registerForm);
            }
        }

        // Create password strength elements if they don't exist
        const strengthContainer = document.getElementById('password-strength-container');
        if (strengthContainer) {
            this.passwordStrengthMeter = document.createElement('meter');
            this.passwordStrengthMeter.id = 'password-strength-meter';
            this.passwordStrengthMeter.min = 0;
            this.passwordStrengthMeter.max = 4;
            this.passwordStrengthMeter.value = 0;

            this.passwordStrengthText = document.createElement('div');
            this.passwordStrengthText.id = 'password-strength-text';
            this.passwordStrengthText.className = 'password-strength-text';
            this.passwordStrengthText.textContent = 'Password strength';

            strengthContainer.appendChild(this.passwordStrengthMeter);
            strengthContainer.appendChild(this.passwordStrengthText);
        }

        // Bind methods to this instance
        this.init = this.init.bind(this);
        this.handleRegister = this.handleRegister.bind(this);
        this.updatePasswordStrength = this.updatePasswordStrength.bind(this);
    }

    // Initialize the registration page
    init() {
        // Check if user is already logged in
        const token = localStorage.getItem('token');
        if (token) {
            window.location.href = 'chat.html';
            return;
        }

        // Add event listeners
        if (this.registerForm) {
            this.registerForm.addEventListener('submit', this.handleRegister);

            if (this.passwordInput) {
                this.passwordInput.addEventListener('input', this.updatePasswordStrength);
            }
        } else {
            console.error('Register form not found');
        }
    }

    // Handle registration form submission
    async handleRegister(e) {
        e.preventDefault();

        // Check if inputs exist
        if (!this.nameInput || !this.emailInput || !this.passwordInput || !this.confirmPasswordInput) {
            this.showError('Form inputs not found');
            console.error('One or more form inputs not found');
            return;
        }

        const name = this.nameInput.value.trim();
        const email = this.emailInput.value.trim();
        const password = this.passwordInput.value.trim();
        const confirmPassword = this.confirmPasswordInput.value.trim();

        // Validate inputs
        if (!name || !email || !password || !confirmPassword) {
            this.showError('Please fill in all fields');
            return;
        }

        if (!validateEmail(email)) {
            this.showError('Please enter a valid email address');
            return;
        }

        const passwordValidation = validatePassword(password);
        if (passwordValidation.score < 2) {
            this.showError(`Password is too weak: ${passwordValidation.message}`);
            return;
        }

        if (password !== confirmPassword) {
            this.showError('Passwords do not match');
            return;
        }

        try {
            // Show loading state
            this.registerForm.classList.add('loading');

            // Call register API
            await authApi.register({ name, email, password });

            // Login automatically after registration
            const loginData = await authApi.login(email, password);

            // Save token and user data
            localStorage.setItem('token', loginData.access_token);
            localStorage.setItem('user', JSON.stringify(loginData.user));

            // Redirect to chat page
            window.location.href = 'chat.html';
        } catch (error) {
            console.error('Registration error:', error);
            this.showError(error.message || 'Registration failed. Please try again.');
        } finally {
            // Hide loading state
            this.registerForm.classList.remove('loading');
        }
    }

    // Update password strength meter
    updatePasswordStrength() {
        if (!this.passwordInput || !this.passwordStrengthMeter || !this.passwordStrengthText) {
            return;
        }

        const password = this.passwordInput.value.trim();
        const strength = validatePassword(password);

        // Update strength meter
        this.passwordStrengthMeter.value = strength.score;
        this.passwordStrengthText.textContent = strength.message;

        // Update strength meter color
        this.passwordStrengthMeter.className = `strength-${strength.score}`;
    }

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
    const registerController = new RegisterController();
    registerController.init();
});

export default RegisterController;
