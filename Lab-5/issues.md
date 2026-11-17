# Lab 5 – Static Code Analysis

## Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded credentials | Security | 7-8 | Wallet PIN and gateway secret are directly stored in source code. | Use environment variables. |
| Weak SHA-1 hashing | Security | 14 | SHA-1 is not suitable for secure PIN hashing. | Replace with PBKDF2-HMAC-SHA256. |
| Insecure temporary file creation | Security | 60 | tempfile.mktemp() can create security vulnerabilities. | Use tempfile.NamedTemporaryFile(). |
| Insecure OTP generation | Security | 64 | random.randint() is not suitable for security-sensitive OTP generation. | Use secrets.randbelow(). |
| Mutable default argument | Bug | 17 | log=[] is shared between function calls. | Change default to None. |
| Unused argument | Code Quality | 50 | merchantType is declared but never used. | Remove or implement the argument. |
| Formatting violations | Style | 76-80 | Missing spaces and blank lines. | Follow PEP 8 formatting. |