// Validation Utilities

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} - True if email is valid
 */
export function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {Object} - Password strength details
 */
export function validatePassword(password) {
    // Empty password
    if (!password) {
        return {
            score: 0,
            message: 'Password is required'
        };
    }
    
    // Calculate password strength
    let score = 0;
    
    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    
    // Character variety checks
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;
    
    // Normalize score to 0-4 range
    score = Math.min(4, Math.floor(score / 1.5));
    
    // Get message based on score
    let message;
    switch (score) {
        case 0:
            message = 'Very weak';
            break;
        case 1:
            message = 'Weak';
            break;
        case 2:
            message = 'Fair';
            break;
        case 3:
            message = 'Good';
            break;
        case 4:
            message = 'Strong';
            break;
        default:
            message = 'Unknown';
    }
    
    return { score, message };
}
