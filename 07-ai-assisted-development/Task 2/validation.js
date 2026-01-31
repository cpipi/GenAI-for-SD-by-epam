/**
 * Data Validation Module
 * Provides validation functions for email, password, and phone number inputs
 * @module validation
 */

/**
 * Validates an email address according to RFC 5322 format
 * @param {string} email - The email address to validate
 * @returns {{valid: boolean, errors: string[]}} Validation result
 */
const validateEmail = (email) => {
  const errors = [];

  // Check for null, undefined, or empty
  if (email === null || email === undefined || email === '') {
    errors.push('Email is required');
    return { valid: false, errors };
  }

  // Convert to string if not already
  const emailStr = String(email).trim();

  // Check length constraints
  if (emailStr.length === 0) {
    errors.push('Email is required');
    return { valid: false, errors };
  }

  // RFC 5322 compliant email regex (simplified but robust)
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

  if (!emailRegex.test(emailStr)) {
    errors.push('Invalid email format');
  }

  // Check local part length (before @)
  const parts = emailStr.split('@');
  if (parts.length !== 2) {
    errors.push('Invalid email format');
  } else {
    const [localPart, domain] = parts;

    if (localPart.length === 0 || localPart.length > 64) {
      errors.push('Email local part must be between 1 and 64 characters');
    }

    // Validate domain has at least one dot and valid structure
    if (!domain.includes('.') || domain.startsWith('.') || domain.endsWith('.')) {
      errors.push('Invalid email domain');
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Validates password strength based on security requirements
 * @param {string} password - The password to validate
 * @returns {{valid: boolean, errors: string[]}} Validation result
 */
const validatePassword = (password) => {
  const errors = [];

  // Check for null, undefined, or empty
  if (password === null || password === undefined || password === '') {
    errors.push('Password is required');
    return { valid: false, errors };
  }

  // Convert to string if not already
  const passwordStr = String(password);

  // Check minimum length
  if (passwordStr.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }

  // Check maximum length (prevent DoS)
  if (passwordStr.length > 128) {
    errors.push('Password must not exceed 128 characters');
  }

  // Check for at least one number
  if (!/\d/.test(passwordStr)) {
    errors.push('Password must contain at least one number');
  }

  // Check for at least one special character
  const specialCharRegex = /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/;
  if (!specialCharRegex.test(passwordStr)) {
    errors.push('Password must contain at least one special character');
  }

  // Check for at least one letter
  if (!/[a-zA-Z]/.test(passwordStr)) {
    errors.push('Password must contain at least one letter');
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Validates phone number in international format
 * @param {string} phone - The phone number to validate
 * @returns {{valid: boolean, errors: string[]}} Validation result
 */
const validatePhone = (phone) => {
  const errors = [];

  // Check for null, undefined, or empty
  if (phone === null || phone === undefined || phone === '') {
    errors.push('Phone number is required');
    return { valid: false, errors };
  }

  // Convert to string if not already
  const phoneStr = String(phone).trim();

  if (phoneStr.length === 0) {
    errors.push('Phone number is required');
    return { valid: false, errors };
  }

  // Must start with +
  if (!phoneStr.startsWith('+')) {
    errors.push('Phone number must start with + and country code');
  }

  // Remove + and allowed formatting characters for digit counting
  const digitsOnly = phoneStr.substring(1).replace(/[\s\-()]/g, '');

  // Check if remaining characters are only digits
  if (!/^\d+$/.test(digitsOnly)) {
    errors.push('Phone number contains invalid characters');
  }

  // Check length (10-15 digits after country code)
  if (digitsOnly.length < 10) {
    errors.push('Phone number must contain between 10 and 15 digits');
  } else if (digitsOnly.length > 15) {
    errors.push('Phone number must contain between 10 and 15 digits');
  }

  // Validate overall format pattern
  const phoneRegex = /^\+\d{1,3}[\s\-]?(\(?\d{1,4}\)?[\s\-]?)?[\d\s\-]{7,}$/;
  if (!phoneRegex.test(phoneStr)) {
    errors.push('Invalid phone number format');
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Validates multiple fields at once
 * @param {Object} data - Object containing fields to validate
 * @param {string} data.email - Email to validate (optional)
 * @param {string} data.password - Password to validate (optional)
 * @param {string} data.phone - Phone number to validate (optional)
 * @returns {{valid: boolean, errors: Object}} Validation results for all fields
 */
const validateAll = (data = {}) => {
  const results = {};
  let allValid = true;

  if (data.email !== undefined) {
    results.email = validateEmail(data.email);
    if (!results.email.valid) allValid = false;
  }

  if (data.password !== undefined) {
    results.password = validatePassword(data.password);
    if (!results.password.valid) allValid = false;
  }

  if (data.phone !== undefined) {
    results.phone = validatePhone(data.phone);
    if (!results.phone.valid) allValid = false;
  }

  return {
    valid: allValid,
    errors: results
  };
};

// Export functions for use in other modules
module.exports = {
  validateEmail,
  validatePassword,
  validatePhone,
  validateAll
};
