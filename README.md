# AI-Driven Framework for Detecting and Preventing Password-Based Attacks

## Project Overview

This project implements a **cryptography-centric authentication framework enhanced with machine learning-based attack detection**.  
The system integrates secure cryptographic primitives with behavioral analysis to detect and prevent password-based attacks such as dictionary attacks, brute-force attempts, and replay attacks.

The framework combines **Argon2 password hashing, Diffie–Hellman key exchange, HMAC-SHA512 authentication, and adaptive ML-based risk detection** to improve the security of password-based authentication systems.

---

## Problem Statement

Password-based authentication remains widely used but is vulnerable to attacks such as dictionary attacks, brute-force attempts, and credential reuse. Traditional systems rely on static password rules and reactive defenses.

This project proposes a **secure authentication framework integrated with machine learning** to analyze authentication behavior and cryptographic signals to detect suspicious login attempts and apply adaptive security responses.

---

## System Architecture

The system consists of five main modules:

### 1. Secure Authentication & Key Management
Handles core cryptographic operations:
- Argon2 password hashing
- Diffie–Hellman key exchange
- HMAC-SHA512 login authentication
- Optional RSA-based session signing
- Password vulnerability scoring

### 2. Attack Simulation
Generates realistic login traffic and simulates:
- Legitimate login attempts
- Dictionary attacks
- Rapid burst attacks
- Low-and-slow attacks
- Replay attacks

### 3. Feature & Risk Intelligence Engine
Extracts authentication features and applies machine learning:
- Password entropy
- Login attempt patterns
- Cryptographic validation signals
- Risk prediction using ML models

### 4. Adaptive Security Control
Applies dynamic security responses based on risk scores:
- CAPTCHA verification
- Temporary account lock
- Permanent lock for high-risk activity

### 5. Monitoring & Security Analytics
Tracks authentication activity and evaluates system performance:
- Event logging
- Detection metrics (accuracy, precision, recall)
- Security analytics and visualization

---

## Key Features

- Argon2 secure password hashing
- Diffie–Hellman session key establishment
- HMAC-SHA512 login authentication
- Machine learning–based attack detection
- Adaptive security control system
- Simulation of multiple password attack strategies
- Security monitoring and analytics

---

## Project Structure
ai-password-attack-detection
│
├── auth
│
├── attacks
│
├── ml_engine
│
├── security_engine
│
├── analytics
│
├── datasets
│
├── main.py
└── README.md