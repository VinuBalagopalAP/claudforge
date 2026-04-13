# Security Policy

## Supported Versions

Currently, the following versions of ClaudForge are supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.2.x   | ✅ |
| 2.0.x   | ✅ |
| < 2.0   | :x:                |

## Security Hardening (v2.2+)

As of v2.2.0, ClaudForge enforces **IRONCLAD Security** for global configurations:
- **Directory Permissions**: The `~/.claudforge` directory is automatically set to `0700` (Owner Read/Write/Execute only). This prevents other system users from accessing your persistent browser profiles, configuration, or upload history.
- **Identity Isolation**: By using the `--profile` discovery system, browser sessions are kept isolated from your default Chrome profile unless explicitly selected.

## Reporting a Vulnerability

We take the security of ClaudForge seriously. If you believe you have found a security vulnerability, please do NOT open a public issue.

Instead, please report it to the maintainer directly at [vinubalagopalap@gmail.com].

Please include:
- A description of the vulnerability.
- Steps to reproduce (if possible).
- Potential impact.

We will acknowledge your report within 48 hours and work with you to resolve the issue before a public disclosure.
