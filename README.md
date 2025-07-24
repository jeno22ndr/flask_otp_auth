# User Login API with Email and OTP Authentication

## Project Overview
This project implements a secure and efficient API system for user authentication using email and One-Time Password (OTP). It allows users to register with their email, request an OTP, and then verify that OTP to gain authenticated access.

## Features
- **Email Registration**: Endpoint to register new users, with email format validation and duplicate checks.
- **OTP Generation & Sending**: Generates a secure OTP and simulates sending it to the user's registered email (prints to console for development).
- **OTP Verification**: Verifies the provided OTP against the stored one, ensuring it's valid and within the time limit.
- **Session Management**: Upon successful OTP verification, a secure JSON Web Token (JWT) is issued for authenticated user sessions.
- **Security Measures**:
    - Basic rate limiting on OTP requests to prevent abuse.
    - Secure algorithms for OTP generation.
    - JWTs for session tokens.

## Technical Stack
- [cite_start]**Backend Framework**: Flask (Python) [cite: 27]
- [cite_start]**Database**: SQLite [cite: 28]
- [cite_start]**Email Service**: Mock service (prints OTP to console) [cite: 29, 30]
- [cite_start]**Token Management**: JWT (JSON Web Tokens) [cite: 31]

## API Endpoints

### 1. User Registration
- [cite_start]**URL**: `/api/register` [cite: 35]
- [cite_start]**Method**: `POST` [cite: 35]
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }

Success Response:
{
  "message": "Registration successful. Please verify your email."
}


2. Request OTP
URL: /api/request-otp 

Method: POST 
Request Body:
{
  "email": "user@example.com"
}

Success Response:
{
  "message": "OTP sent to your email."
}
(Note: The OTP will be printed to the console where the Flask server is running.)


3. Verify OTP
URL: /api/verify-otp
Method: POST 
Request Body:
{
  "email": "user@example.com",
  "otp": "123456"
}
Success Response:
{
  "message": "Login successful.",
  "token": "jwt_token_string_here"
}
