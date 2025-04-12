// Password Strength Meter and Form Validation

document.addEventListener('DOMContentLoaded', function() {
    // Initialize password strength meter if on register page
    const passwordInput = document.getElementById('register-password');
    const confirmPasswordInput = document.getElementById('register-confirm-password');

    if (passwordInput) {
        initPasswordStrengthMeter(passwordInput);
    }

    // Initialize form validation
    initFormValidation();
});

// Password strength meter
function initPasswordStrengthMeter(passwordInput) {
    // Get the container for the password strength meter
    const meterContainer = document.getElementById('password-strength-container');

    // If container exists, populate it
    if (meterContainer) {
        meterContainer.innerHTML = `
            <div class="password-strength-meter">
                <div class="password-strength-meter-fill"></div>
            </div>
            <div class="password-strength-text">
                <span class="password-strength-label">Strength: <span class="strength-text">None</span></span>
                <span class="password-strength-score">Score: <span class="score-value">0/100</span></span>
            </div>
            <div class="password-requirements">
                <div class="password-requirement" data-requirement="length">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 8 characters</span>
                </div>
                <div class="password-requirement" data-requirement="lowercase">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 lowercase letter</span>
                </div>
                <div class="password-requirement" data-requirement="uppercase">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 uppercase letter</span>
                </div>
                <div class="password-requirement" data-requirement="number">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 number</span>
                </div>
                <div class="password-requirement" data-requirement="special">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 special character</span>
                </div>
            </div>
        `;
    } else {
        // If no container exists, create one and insert after password input
        const newMeterContainer = document.createElement('div');
        newMeterContainer.className = 'password-strength-container';
        newMeterContainer.innerHTML = `
            <div class="password-strength-meter">
                <div class="password-strength-meter-fill"></div>
            </div>
            <div class="password-strength-text">
                <span class="password-strength-label">Strength: <span class="strength-text">None</span></span>
                <span class="password-strength-score">Score: <span class="score-value">0/100</span></span>
            </div>
            <div class="password-requirements">
                <div class="password-requirement" data-requirement="length">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 8 characters</span>
                </div>
                <div class="password-requirement" data-requirement="lowercase">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 lowercase letter</span>
                </div>
                <div class="password-requirement" data-requirement="uppercase">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 uppercase letter</span>
                </div>
                <div class="password-requirement" data-requirement="number">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 number</span>
                </div>
                <div class="password-requirement" data-requirement="special">
                    <i class="fas fa-times-circle requirement-unmet"></i>
                    <span>At least 1 special character</span>
                </div>
            </div>
        `;

        // Insert after password input
        passwordInput.parentNode.insertBefore(newMeterContainer, passwordInput.nextSibling);
        // Use the new container
        return initPasswordStrengthMeter(passwordInput);
    }

    // Get elements
    const strengthMeter = meterContainer.querySelector('.password-strength-meter');
    const strengthFill = meterContainer.querySelector('.password-strength-meter-fill');
    const strengthText = meterContainer.querySelector('.strength-text');
    const scoreValue = meterContainer.querySelector('.score-value');
    const requirements = meterContainer.querySelectorAll('.password-requirement');

    // Add event listener to password input
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const result = calculatePasswordStrength(password);

        // Update meter
        strengthMeter.className = 'password-strength-meter strength-' + result.strengthClass;
        strengthFill.style.width = result.score + '%';
        strengthText.textContent = result.strengthText;
        scoreValue.textContent = result.score + '/100';

        // Update requirements
        updateRequirements(password, requirements);
    });
}

// Calculate password strength
function calculatePasswordStrength(password) {
    // Base score
    let score = 0;
    let strengthClass = 'very-weak';
    let strengthText = 'Very Weak';

    if (!password) {
        return { score: 0, strengthClass: 'very-weak', strengthText: 'None' };
    }

    // Length contribution (up to 25 points)
    const lengthScore = Math.min(25, password.length * 2);
    score += lengthScore;

    // Character variety contribution
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[^a-zA-Z0-9]/.test(password);

    // Add points for variety (up to 25 points)
    const varietyScore = (hasLower ? 5 : 0) + (hasUpper ? 5 : 0) +
                         (hasNumber ? 5 : 0) + (hasSpecial ? 10 : 0);
    score += varietyScore;

    // Complexity contribution (up to 50 points)
    // Check for patterns, repetitions, etc.
    const hasSequence = /abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789/i.test(password);
    const hasRepetition = /(.)\1{2,}/i.test(password); // Same character 3+ times in a row

    // Deduct points for patterns (up to -20 points)
    const patternPenalty = (hasSequence ? -10 : 0) + (hasRepetition ? -10 : 0);
    score = Math.max(0, score + patternPenalty);

    // Add bonus for length and complexity combined
    if (password.length >= 12 && hasLower && hasUpper && hasNumber && hasSpecial) {
        score = Math.min(100, score + 20); // Bonus points, max 100
    }

    // Determine strength text and class
    if (score >= 90) {
        strengthClass = 'very-strong';
        strengthText = 'Very Strong';
    } else if (score >= 70) {
        strengthClass = 'strong';
        strengthText = 'Strong';
    } else if (score >= 50) {
        strengthClass = 'medium';
        strengthText = 'Medium';
    } else if (score >= 30) {
        strengthClass = 'weak';
        strengthText = 'Weak';
    } else {
        strengthClass = 'very-weak';
        strengthText = 'Very Weak';
    }

    return { score, strengthClass, strengthText };
}

// Update password requirements
function updateRequirements(password, requirements) {
    const checks = {
        length: password.length >= 8,
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^a-zA-Z0-9]/.test(password)
    };

    requirements.forEach(req => {
        const type = req.getAttribute('data-requirement');
        const icon = req.querySelector('i');

        if (checks[type]) {
            icon.className = 'fas fa-check-circle requirement-met';
        } else {
            icon.className = 'fas fa-times-circle requirement-unmet';
        }
    });
}

// Form validation
function initFormValidation() {
    // Login form validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        const emailInput = document.getElementById('login-email');
        const passwordInput = document.getElementById('login-password');

        // Email validation
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });

        // Password validation (just check if not empty for login)
        passwordInput.addEventListener('blur', function() {
            validateRequired(this, 'Password is required');
        });

        // Form submission validation
        loginForm.addEventListener('submit', function(e) {
            const isEmailValid = validateEmail(emailInput);
            const isPasswordValid = validateRequired(passwordInput, 'Password is required');

            if (!isEmailValid || !isPasswordValid) {
                e.preventDefault();
            }
        });
    }

    // Register form validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        const nameInput = document.getElementById('register-name');
        const emailInput = document.getElementById('register-email');
        const passwordInput = document.getElementById('register-password');
        const confirmPasswordInput = document.getElementById('register-confirm-password');

        // Name validation
        nameInput.addEventListener('blur', function() {
            validateRequired(this, 'Name is required');
        });

        // Email validation
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });

        // Password validation
        passwordInput.addEventListener('blur', function() {
            validatePassword(this);
        });

        // Confirm password validation
        confirmPasswordInput.addEventListener('blur', function() {
            validateConfirmPassword(this, passwordInput);
        });

        // Update confirm password validation when password changes
        passwordInput.addEventListener('input', function() {
            if (confirmPasswordInput.value) {
                validateConfirmPassword(confirmPasswordInput, passwordInput);
            }
        });

        // Form submission validation
        registerForm.addEventListener('submit', function(e) {
            const isNameValid = validateRequired(nameInput, 'Name is required');
            const isEmailValid = validateEmail(emailInput);
            const isPasswordValid = validatePassword(passwordInput);
            const isConfirmPasswordValid = validateConfirmPassword(confirmPasswordInput, passwordInput);

            if (!isNameValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
                e.preventDefault();
            }
        });
    }
}

// Validate required field
function validateRequired(input, errorMessage) {
    const formGroup = input.closest('.form-group');
    clearValidation(formGroup);

    if (!input.value.trim()) {
        showError(formGroup, errorMessage || 'This field is required');
        return false;
    } else {
        showSuccess(formGroup);
        return true;
    }
}

// Validate email
function validateEmail(input) {
    const formGroup = input.closest('.form-group');
    clearValidation(formGroup);

    if (!input.value.trim()) {
        showError(formGroup, 'Email is required');
        return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(input.value)) {
        showError(formGroup, 'Please enter a valid email address');
        return false;
    } else {
        showSuccess(formGroup);
        return true;
    }
}

// Validate password
function validatePassword(input) {
    const formGroup = input.closest('.form-group');
    clearValidation(formGroup);

    if (!input.value) {
        showError(formGroup, 'Password is required');
        return false;
    }

    if (input.value.length < 8) {
        showError(formGroup, 'Password must be at least 8 characters');
        return false;
    }

    // Check for at least 3 of the 4 requirements
    const hasLower = /[a-z]/.test(input.value);
    const hasUpper = /[A-Z]/.test(input.value);
    const hasNumber = /[0-9]/.test(input.value);
    const hasSpecial = /[^a-zA-Z0-9]/.test(input.value);

    const requirementsMet = [hasLower, hasUpper, hasNumber, hasSpecial].filter(Boolean).length;

    if (requirementsMet < 3) {
        showError(formGroup, 'Password must meet at least 3 of the 4 requirements');
        return false;
    } else {
        showSuccess(formGroup);
        return true;
    }
}

// Validate confirm password
function validateConfirmPassword(input, passwordInput) {
    const formGroup = input.closest('.form-group');
    clearValidation(formGroup);

    if (!input.value) {
        showError(formGroup, 'Please confirm your password');
        return false;
    }

    if (input.value !== passwordInput.value) {
        showError(formGroup, 'Passwords do not match');
        return false;
    } else {
        showSuccess(formGroup);
        return true;
    }
}

// Show error message
function showError(formGroup, message) {
    formGroup.classList.add('error');
    formGroup.classList.remove('success');

    // Remove existing validation message if any
    const existingMessage = formGroup.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'validation-message validation-error';
    errorDiv.innerHTML = `
        <span class="validation-icon">
            <span class="cross"></span>
        </span>
        ${message}
    `;

    // Add after input
    const input = formGroup.querySelector('input');
    input.parentNode.insertBefore(errorDiv, input.nextSibling);
}

// Show success message
function showSuccess(formGroup) {
    formGroup.classList.add('success');
    formGroup.classList.remove('error');

    // Remove existing validation message if any
    const existingMessage = formGroup.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // Create success message
    const successDiv = document.createElement('div');
    successDiv.className = 'validation-message validation-success';
    successDiv.innerHTML = `
        <span class="validation-icon">
            <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
        </span>
        Valid
    `;

    // Add after input
    const input = formGroup.querySelector('input');
    input.parentNode.insertBefore(successDiv, input.nextSibling);
}

// Clear validation
function clearValidation(formGroup) {
    formGroup.classList.remove('error', 'success');

    // Remove existing validation message if any
    const existingMessage = formGroup.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }
}
