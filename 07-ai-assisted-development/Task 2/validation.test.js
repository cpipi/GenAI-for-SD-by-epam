/**
 * Unit Tests for Data Validation Module
 * Testing validateEmail, validatePassword, and validatePhone functions
 * @jest-environment node
 */

const {
  validateEmail,
  validatePassword,
  validatePhone,
  validateAll
} = require('./validation');

describe('Email Validation Tests', () => {
  describe('Valid email addresses', () => {
    test('should validate a standard email', () => {
      const result = validateEmail('user@example.com');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate email with subdomain', () => {
      const result = validateEmail('john.doe@mail.company.co.uk');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate email with plus sign', () => {
      const result = validateEmail('user+tag@example.com');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate email with numbers', () => {
      const result = validateEmail('user123@example456.com');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
  });

  describe('Invalid email addresses', () => {
    test('should reject null email', () => {
      const result = validateEmail(null);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Email is required');
    });

    test('should reject empty string', () => {
      const result = validateEmail('');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Email is required');
    });

    test('should reject email without @ symbol', () => {
      const result = validateEmail('userexample.com');
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should reject email without domain', () => {
      const result = validateEmail('user@');
      expect(result.valid).toBe(false);
      expect(result.errors.some(err => err.includes('domain'))).toBe(true);
    });

    test('should reject email with spaces', () => {
      const result = validateEmail('user name@example.com');
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should reject email with invalid characters', () => {
      const result = validateEmail('user@exa mple.com');
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });
  });
});

describe('Password Validation Tests', () => {
  describe('Valid passwords', () => {
    test('should validate password with all requirements', () => {
      const result = validatePassword('SecurePass123!');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate password with multiple special characters', () => {
      const result = validatePassword('MyP@ssw0rd!');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate long password', () => {
      const result = validatePassword('VeryLongPassword123!WithMoreCharacters');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
  });

  describe('Invalid passwords', () => {
    test('should reject null password', () => {
      const result = validatePassword(null);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password is required');
    });

    test('should reject empty password', () => {
      const result = validatePassword('');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password is required');
    });

    test('should reject password shorter than 8 characters', () => {
      const result = validatePassword('Short1!');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password must be at least 8 characters long');
    });

    test('should reject password without numbers', () => {
      const result = validatePassword('NoNumbers!');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password must contain at least one number');
    });

    test('should reject password without special characters', () => {
      const result = validatePassword('NoSpecial123');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password must contain at least one special character');
    });

    test('should reject password without letters', () => {
      const result = validatePassword('12345678!');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password must contain at least one letter');
    });

    test('should reject password that is too long', () => {
      const longPassword = 'a'.repeat(130) + '1!';
      const result = validatePassword(longPassword);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password must not exceed 128 characters');
    });

    test('should reject password with multiple violations', () => {
      const result = validatePassword('weak');
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThanOrEqual(2);
      expect(result.errors).toContain('Password must be at least 8 characters long');
      expect(result.errors).toContain('Password must contain at least one number');
    });
  });
});

describe('Phone Number Validation Tests', () => {
  describe('Valid phone numbers', () => {
    test('should validate phone with country code', () => {
      const result = validatePhone('+1234567890');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate phone with spaces', () => {
      const result = validatePhone('+44 20 7946 0958');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate phone with hyphens', () => {
      const result = validatePhone('+1-555-123-4567');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('should validate phone with parentheses', () => {
      const result = validatePhone('+1 (555) 123-4567');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
  });

  describe('Invalid phone numbers', () => {
    test('should reject null phone number', () => {
      const result = validatePhone(null);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number is required');
    });

    test('should reject empty phone number', () => {
      const result = validatePhone('');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number is required');
    });

    test('should reject phone without + prefix', () => {
      const result = validatePhone('1234567890');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number must start with + and country code');
    });

    test('should reject phone that is too short', () => {
      const result = validatePhone('+123');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number must contain between 10 and 15 digits');
    });

    test('should reject phone that is too long', () => {
      const result = validatePhone('+12345678901234567890');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number must contain between 10 and 15 digits');
    });

    test('should reject phone with letters', () => {
      const result = validatePhone('+123abc4567890');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number contains invalid characters');
    });
  });
});

describe('Edge Cases and Special Inputs', () => {
  describe('Email edge cases', () => {
    test('should handle undefined email', () => {
      const result = validateEmail(undefined);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Email is required');
    });

    test('should handle whitespace-only email', () => {
      const result = validateEmail('   ');
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should handle email with multiple @ symbols', () => {
      const result = validateEmail('user@@example.com');
      expect(result.valid).toBe(false);
    });
  });

  describe('Password edge cases', () => {
    test('should handle undefined password', () => {
      const result = validatePassword(undefined);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password is required');
    });

    test('should handle numeric input for password', () => {
      const result = validatePassword(12345678);
      expect(result.valid).toBe(false);
      // Should convert to string and validate
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should validate password with exactly 8 characters', () => {
      const result = validatePassword('Valid123!');
      expect(result.valid).toBe(true);
    });
  });

  describe('Phone edge cases', () => {
    test('should handle undefined phone', () => {
      const result = validatePhone(undefined);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number is required');
    });

    test('should handle phone with only + sign', () => {
      const result = validatePhone('+');
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('should handle phone with special characters', () => {
      const result = validatePhone('+123#456@7890');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Phone number contains invalid characters');
    });
  });
});

describe('validateAll function', () => {
  test('should validate multiple fields at once - all valid', () => {
    const result = validateAll({
      email: 'user@example.com',
      password: 'SecurePass123!',
      phone: '+1234567890'
    });
    expect(result.valid).toBe(true);
    expect(result.errors.email.valid).toBe(true);
    expect(result.errors.password.valid).toBe(true);
    expect(result.errors.phone.valid).toBe(true);
  });

  test('should validate multiple fields - some invalid', () => {
    const result = validateAll({
      email: 'invalid-email',
      password: 'weak',
      phone: '+1234567890'
    });
    expect(result.valid).toBe(false);
    expect(result.errors.email.valid).toBe(false);
    expect(result.errors.password.valid).toBe(false);
    expect(result.errors.phone.valid).toBe(true);
  });

  test('should handle partial validation', () => {
    const result = validateAll({
      email: 'user@example.com'
    });
    expect(result.errors.email.valid).toBe(true);
    expect(result.errors.password).toBeUndefined();
    expect(result.errors.phone).toBeUndefined();
  });

  test('should handle empty object', () => {
    const result = validateAll({});
    expect(result.valid).toBe(true);
    expect(Object.keys(result.errors)).toHaveLength(0);
  });
});

describe('Performance tests', () => {
  test('should validate email quickly', () => {
    const start = Date.now();
    for (let i = 0; i < 1000; i++) {
      validateEmail('test@example.com');
    }
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(100); // Should complete 1000 validations in < 100ms
  });

  test('should validate password quickly', () => {
    const start = Date.now();
    for (let i = 0; i < 1000; i++) {
      validatePassword('SecurePass123!');
    }
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(100);
  });

  test('should validate phone quickly', () => {
    const start = Date.now();
    for (let i = 0; i < 1000; i++) {
      validatePhone('+1234567890');
    }
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(100);
  });
});
