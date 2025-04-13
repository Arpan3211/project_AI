// Authentication Service for Login and Register Pages

// Get API URL from config
const API_URL = window.appConfig.API_URL;

// Show loading spinner
function showLoading(form) {
    // Disable submit button and show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Loading...';
}

// Hide loading spinner
function hideLoading(form, originalText = 'Submit') {
    // Enable submit button and hide loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
}

// Show error message
function showError(form, message) {
    // Remove any existing error message
    const existingError = form.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    // Create and append error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    form.appendChild(errorDiv);
}

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        // Handle login form submission
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            showLoading(loginForm);
            login(email, password, loginForm);
        });
    }

    // Check if we're on the register page
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        // Handle register form submission
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            const confirmPassword = document.getElementById('register-confirm-password').value;

            if (password !== confirmPassword) {
                showError(registerForm, 'Passwords do not match');
                return;
            }

            showLoading(registerForm);
            register(name, email, password, registerForm);
        });
    }
});

// Login function
async function login(email, password, form) {
    try {
        // Create form data for OAuth2 password flow
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        // Send login request
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        // Save token to localStorage
        localStorage.setItem('token', data.access_token);

        // Get user profile
        const userResponse = await fetch(`${API_URL}/auth/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${data.access_token}`,
            },
        });

        if (!userResponse.ok) {
            throw new Error('Failed to fetch user profile');
        }

        const userData = await userResponse.json();

        // Save user data to localStorage
        localStorage.setItem('user', JSON.stringify(userData));

        // Redirect to chat page
        window.location.href = 'chat.html';
    } catch (error) {
        console.error('Login error:', error);
        hideLoading(form, 'Login');
        showError(form, error.message || 'Login failed. Please try again.');
    }
}

// Register function
async function register(name, email, password, form) {
    try {
        // Validate inputs
        if (!name || name.trim() === '') {
            throw new Error('Name is required');
        }

        if (!email || !isValidEmail(email)) {
            throw new Error('Please enter a valid email address');
        }

        if (!password || password.length < 6) {
            throw new Error('Password must be at least 6 characters');
        }

        // Send registration request
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name.trim(),
                email: email.trim(),
                password
            })
        });

        let data;
        try {
            data = await response.json();
        } catch (e) {
            console.error('Error parsing response:', e);
            throw new Error('Server error. Please try again later.');
        }

        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }

        // Registration successful - redirect to login page
        hideLoading(form);
        alert('Registration successful! Please login with your credentials.');
        window.location.href = 'login.html';
    } catch (error) {
        console.error('Registration error:', error);
        hideLoading(form, 'Register');
        showError(form, error.message || 'Registration failed. Please try again.');
    }
}

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Fetch and store user profile
async function fetchAndStoreUserProfile() {
    try {
        const token = localStorage.getItem('token');
        if (!token) return null;

        const response = await fetch(`${API_URL}/auth/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user profile');
        }

        const userData = await response.json();
        localStorage.setItem('currentUser', JSON.stringify(userData));
        return userData;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('currentUser');
        return null;
    }
}
