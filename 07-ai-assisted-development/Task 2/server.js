/**
 * Simple Express.js Server for Data Validation Module
 * Implements REST API endpoints for validation
 */

const express = require('express');
const { Pool } = require('pg');
const { validateEmail, validatePassword, validatePhone } = require('./validation');

const app = express();
const PORT = process.env.PORT || 3000;

// Database connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost/validation_db',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// CORS middleware (enable for production with specific origins)
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Routes

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// POST /api/v1/validate - Validate input data
app.post('/api/v1/validate', async (req, res) => {
  try {
    const { type, value } = req.body;

    // Validate request
    if (!type || value === undefined) {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'Both type and value are required'
      });
    }

    // Perform validation based on type
    let result;
    switch (type.toLowerCase()) {
      case 'email':
        result = validateEmail(value);
        break;
      case 'password':
        result = validatePassword(value);
        break;
      case 'phone':
        result = validatePhone(value);
        break;
      default:
        return res.status(400).json({
          error: 'Invalid request',
          message: 'Type must be one of: email, password, phone'
        });
    }

    // Log validation attempt (optional - for analytics)
    // You could log to database here

    res.json(result);
  } catch (error) {
    console.error('Validation error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'An unexpected error occurred'
    });
  }
});

// GET /api/v1/validation-rules - Get validation rules from database
app.get('/api/v1/validation-rules', async (req, res) => {
  try {
    const { type, active = 'true' } = req.query;

    let query = 'SELECT * FROM validation_rules WHERE is_active = $1';
    const params = [active === 'true'];

    if (type) {
      query += ' AND rule_type = $2 ORDER BY priority';
      params.push(type.toLowerCase());
    } else {
      query += ' ORDER BY rule_type, priority';
    }

    const result = await pool.query(query, params);

    res.json({
      success: true,
      count: result.rows.length,
      data: result.rows
    });
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({
      success: false,
      error: 'Database connection failed',
      message: error.message
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: 'The requested endpoint does not exist'
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'An error occurred'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n=================================`);
  console.log(`Data Validation API Server`);
  console.log(`=================================`);
  console.log(`Server running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`\nEndpoints:`);
  console.log(`  GET  /health`);
  console.log(`  POST /api/v1/validate`);
  console.log(`  GET  /api/v1/validation-rules`);
  console.log(`=================================\n`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  pool.end(() => {
    console.log('Database pool closed');
    process.exit(0);
  });
});

module.exports = app;
