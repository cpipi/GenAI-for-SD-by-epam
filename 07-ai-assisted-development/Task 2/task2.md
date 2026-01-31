Task: Build a Data Validation Module Using ChatGPT

Objective: Learn how to use ChatGPT to generate, test, and document production-ready code for a real feature.

Feature: Data Validation Module - validates user input (email, password, phone) with custom rules and error messages.

Steps

Define Requirements
Prompt ChatGPT: "List requirements for a data validation module that validates: email format, password strength (8+ chars, 1 number, 1 special char), phone number (international format). Include error messages for each rule"
Review and confirm requirements
Generate Backend Code
Prompt: "Write a Node.js validation module with functions: validateEmail(), validatePassword(), validatePhone(). Include error handling and return format: {valid: boolean, errors: []}. Use modern JavaScript (ES6+)"
Test the code logic mentally or in ChatGPT
Create Database Schema & API
Prompt: "Design a database schema for storing validation rules (rule_name, regex_pattern, error_message). Create 2 REST API endpoints: POST /validate (validates data) and GET /validation-rules (returns all rules). Provide SQL and endpoint specifications"
Review schema structure
Generate Unit Tests
Prompt: "Write Jest unit tests for the validation module. Cover: valid inputs, invalid inputs, edge cases (empty strings, null, special characters). Provide 10 test cases"
Check test coverage
Create Documentation
Prompt: "Write API documentation in Markdown format including: Overview, Installation, Usage Examples, API Endpoints (request/response), Error Codes, Example Code"
Ensure examples are clear
Validate & Refine
Prompt: "Review this validation module for: security vulnerabilities (SQL injection, XSS), performance (can handle 1000 requests/sec), and code quality (readable, maintainable). Suggest improvements"
Apply critical suggestions
Deliverable: A document with sections: Requirements Document (validation rules table), Source Code (validation.js file ~100 lines), Database Schema (SQL file), API Specification (endpoint details), Unit Tests (validation.test.js with 10+ tests), README.md (installation + usage guide)

Tools: ChatGPT + VS Code/Google Docs + (optional) Node.js for testing


Grading Criteria
Your assignment will be evaluated based on the completeness and quality of the following deliverables:

Requirements Document (10 pts)
Clear validation rules table for email/password/phone
Specific criteria and error messages
Source Code (25 pts)
Functional validation.js (~100 lines)
validateEmail(), validatePassword(), validatePhone() functions
Proper error handling
Returns {valid: boolean, errors: []} format
Uses modern ES6+ syntax
Database Schema & API (20 pts)
SQL schema for validation_rules table (rule_name, regex_pattern, error_message)
Specifications for POST /validate and GET /validation-rules endpoints
Request/response examples included
Unit Tests (25 pts)
validation.test.js with 10+ Jest test cases
Covers valid inputs, invalid inputs, and edge cases
Tests empty strings, null, and special characters
Documentation (15 pts)
Complete README.md with:
Overview
Installation
Usage Examples
API Endpoints
Error Codes
Example Code
Validation & Refinement (5 pts)
Evidence of security/performance/code quality review
Applied improvements demonstrated

Grading Scale
You can earn a maximum of 100 points for completing this task.

90-100 (A): All sections complete, code works, 10+ tests, comprehensive documentation, refinements applied
80-89 (B): All sections present, code functional, 8-10 tests, good documentation, minor gaps
70-79 (C): Most sections present, code has issues, 5-7 tests, basic documentation
<70 (F): Missing deliverables, non-functional code, or minimal effort

Instructions for Submitting Your Task 
Name your file as follows: Module Name_PT2_[your_name]_[your_last_name]. Submit your response in the form below, attaching the file in your preferred format—docx, txt or pdf.