-- ============================================
-- Data Validation Module - Database Schema
-- ============================================
-- Database: PostgreSQL (compatible with MySQL with minor syntax changes)
-- Purpose: Store validation rules and patterns

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS validation_logs;
DROP TABLE IF EXISTS validation_rules;

-- ============================================
-- Table: validation_rules
-- Purpose: Store validation rules with regex patterns and error messages
-- ============================================

CREATE TABLE validation_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL UNIQUE,
    rule_type VARCHAR(50) NOT NULL CHECK (rule_type IN ('email', 'password', 'phone')),
    regex_pattern TEXT NOT NULL,
    error_message TEXT NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) DEFAULT 'system'
);

-- Create index for faster queries
CREATE INDEX idx_validation_rules_type ON validation_rules(rule_type);
CREATE INDEX idx_validation_rules_active ON validation_rules(is_active);

-- ============================================
-- Table: validation_logs
-- Purpose: Log validation attempts for auditing and analytics
-- ============================================

CREATE TABLE validation_logs (
    id SERIAL PRIMARY KEY,
    validation_type VARCHAR(50) NOT NULL,
    input_value_hash VARCHAR(64),  -- Store hash for privacy
    is_valid BOOLEAN NOT NULL,
    error_count INTEGER DEFAULT 0,
    validation_time_ms DECIMAL(10,3),
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for analytics queries
CREATE INDEX idx_validation_logs_type ON validation_logs(validation_type);
CREATE INDEX idx_validation_logs_created ON validation_logs(created_at);

-- ============================================
-- Insert default validation rules
-- ============================================

-- Email validation rules
INSERT INTO validation_rules (rule_name, rule_type, regex_pattern, error_message, description, priority) VALUES
('email_required', 'email', '^.+$', 'Email is required', 'Checks if email is not empty', 1),
('email_format', 'email', '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$', 'Invalid email format', 'RFC 5322 compliant email format', 2),
('email_local_length', 'email', '^[^@]{1,64}@', 'Email local part must be between 1 and 64 characters', 'Validates local part length', 3),
('email_domain', 'email', '@.+\..+$', 'Invalid email domain', 'Ensures domain has proper structure', 4);

-- Password validation rules
INSERT INTO validation_rules (rule_name, rule_type, regex_pattern, error_message, description, priority) VALUES
('password_required', 'password', '^.+$', 'Password is required', 'Checks if password is not empty', 1),
('password_length_min', 'password', '^.{8,}$', 'Password must be at least 8 characters long', 'Minimum length requirement', 2),
('password_length_max', 'password', '^.{1,128}$', 'Password must not exceed 128 characters', 'Maximum length limit', 3),
('password_number', 'password', '.*\d.*', 'Password must contain at least one number', 'Requires numeric character', 4),
('password_special', 'password', '.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?].*', 'Password must contain at least one special character', 'Requires special character', 5),
('password_letter', 'password', '.*[a-zA-Z].*', 'Password must contain at least one letter', 'Requires alphabetic character', 6);

-- Phone validation rules
INSERT INTO validation_rules (rule_name, rule_type, regex_pattern, error_message, description, priority) VALUES
('phone_required', 'phone', '^.+$', 'Phone number is required', 'Checks if phone is not empty', 1),
('phone_format', 'phone', '^\+\d{1,3}[\s\-]?(\(?\d{1,4}\)?[\s\-]?)?[\d\s\-]{7,}$', 'Invalid phone number format', 'International format with + prefix', 2),
('phone_prefix', 'phone', '^\+', 'Phone number must start with + and country code', 'Requires + prefix', 3),
('phone_length', 'phone', '^\+\d{10,15}$', 'Phone number must contain between 10 and 15 digits', 'Length validation', 4);

-- ============================================
-- Useful queries
-- ============================================

-- Query to get all active rules for a specific type
-- SELECT * FROM validation_rules WHERE rule_type = 'email' AND is_active = TRUE ORDER BY priority;

-- Query to get validation statistics
-- SELECT validation_type, COUNT(*) as total_validations, 
--        SUM(CASE WHEN is_valid THEN 1 ELSE 0 END) as successful,
--        AVG(validation_time_ms) as avg_time_ms
-- FROM validation_logs 
-- GROUP BY validation_type;

-- ============================================
-- Update trigger for updated_at timestamp
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_validation_rules_updated_at
    BEFORE UPDATE ON validation_rules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Grant permissions (adjust as needed)
-- ============================================

-- GRANT SELECT, INSERT ON validation_rules TO app_user;
-- GRANT SELECT, INSERT ON validation_logs TO app_user;

-- ============================================
-- End of schema
-- ============================================
