// Authentication Service for Chat Page

// Get API URL from config
const API_URL = window.appConfig.API_URL;

// User authentication state
let currentUser = null;

// Initialize auth service
async function initAuth() {
    // Check if token exists
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('currentUser');

    if (token && savedUser) {
        try {
            // Validate token by fetching user profile
            const response = await fetch(`${API_URL}/auth/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                // Token is valid, update user profile
                const userData = await response.json();
                currentUser = userData;
                localStorage.setItem('currentUser', JSON.stringify(userData));
                updateUserProfile(userData);
            } else {
                // Token is invalid, clear auth data
                clearAuthData();
                showLoginButton();
            }
        } catch (error) {
            console.error('Error validating token:', error);
            clearAuthData();
            showLoginButton();
        }
    } else if (savedUser) {
        // We have user data but no token (old implementation)
        currentUser = JSON.parse(savedUser);
        updateUserProfile(currentUser);
    } else {
        // No authentication data
        showLoginButton();
    }

    // Setup user menu click outside
    document.addEventListener('click', (e) => {
        const userMenu = document.querySelector('.user-menu');
        if (userMenu && !e.target.closest('.user-profile') && !e.target.closest('.user-menu')) {
            userMenu.classList.remove('active');
        }
    });
}

// Show login button
function showLoginButton() {
    const userProfile = document.getElementById('user-profile');
    if (userProfile) {
        userProfile.innerHTML = '<div class="user-badge" id="login-btn">Login</div>';

        // Add event listener to login button
        const loginBtn = document.getElementById('login-btn');
        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                window.location.href = 'login.html';
            });
        }
    }
}

// Clear authentication data
function clearAuthData() {
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    currentUser = null;
}

// Logout function
async function logout() {
    try {
        const token = localStorage.getItem('token');
        if (token) {
            // Call the logout API to blacklist the token
            const response = await fetch(`${API_URL}/auth/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                mode: 'cors',
                credentials: 'include'
            });

            if (!response.ok) {
                console.error('Error logging out:', await response.text());
            }
        }
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        // Clear authentication data regardless of API success
        clearAuthData();

        // Update UI
        showLoginButton();

        // Remove user menu if exists
        const userMenu = document.querySelector('.user-menu');
        if (userMenu) {
            userMenu.remove();
        }
    }
}

// Update user profile in UI
function updateUserProfile(user) {
    const userProfile = document.getElementById('user-profile');

    // Create user avatar SVG
    const userAvatar = `
        <svg class="user-avatar" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="12" fill="#e5e7eb"/>
            <circle cx="12" cy="9" r="4" fill="#9ca3af"/>
            <path d="M4 20.5C4 16.9 7.6 14 12 14C16.4 14 20 16.9 20 20.5" stroke="#9ca3af" stroke-width="2"/>
        </svg>
    `;

    // Update user profile
    userProfile.innerHTML = `
        <div class="user-info" id="user-info">
            ${userAvatar}
            <span class="user-name">${user.name}</span>
        </div>
    `;

    // Create user menu
    const userMenu = document.createElement('div');
    userMenu.className = 'user-menu';
    userMenu.innerHTML = `
        <div class="user-menu-item">
            <i class="fas fa-user"></i>
            <span>Profile</span>
        </div>
        <div class="user-menu-item">
            <i class="fas fa-cog"></i>
            <span>Settings</span>
        </div>
        <div class="user-menu-item" id="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            <span>Logout</span>
        </div>
    `;

    userProfile.appendChild(userMenu);

    // Add event listener to user info
    document.getElementById('user-info').addEventListener('click', toggleUserMenu);

    // Add event listener to logout button
    document.getElementById('logout-btn').addEventListener('click', logout);
}

// Toggle user menu
function toggleUserMenu() {
    const userMenu = document.querySelector('.user-menu');
    if (userMenu) {
        userMenu.classList.toggle('active');
    }
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', initAuth);
