# Secure Coding Review
### CodeAlpha Cybersecurity Internship — Task 3

A static security analysis of a deliberately vulnerable Python application using **Bandit**, an industry-standard Python security linter. Includes a full findings report with remediation steps for every vulnerability detected.

---

## Overview

Insecure code is one of the leading causes of data breaches. This project demonstrates how to perform a security-focused code review using Bandit, identify vulnerabilities across multiple severity levels, and provide actionable remediation steps for each finding.

---

## Files

| File | Description |
|------|-------------|
| `vulnerable_app.py` | Deliberately insecure Python app (audit target) |
| `bandit_output.txt` | Raw Bandit scan output |
| `findings_report.md` | Full vulnerability report with remediations |

---

## How to Reproduce

**Install Bandit:**
```bash
pip install bandit
```

**Run the scan:**
```bash
python -m bandit -r vulnerable_app.py
```

**Save output to file:**
```bash
python -m bandit -r vulnerable_app.py -o bandit_output.txt -f txt
```

---

## Vulnerabilities Found

| Bandit ID | Severity | Vulnerability |
|-----------|----------|--------------|
| B324 | High | MD5 used for password hashing |
| B605 | High | Command injection via os.system() |
| B602 | High | subprocess with shell=True |
| B608 | Medium | SQL injection via string concatenation |
| B301 | Medium | Insecure deserialization (pickle.loads) |
| B307 | Medium | Use of eval() on user input |
| B506 | Medium | yaml.load() without safe loader |
| B403 | Low | pickle module imported |
| B404 | Low | subprocess module imported |
| B105 | Low | Hardcoded password (SECRET_KEY) |
| B105 | Low | Hardcoded password (DB_PASSWORD) |
| B101 | Low | assert used for security check |
| B311 | Low | Insecure random for token generation |

**Total: 3 High, 4 Medium, 6 Low**

---

## Skills Demonstrated

- Static analysis using Bandit
- Vulnerability identification and classification (CWE mapping)
- Secure coding principles (OWASP Top 10)
- Python security best practices
- Technical documentation and reporting

---

## Author

**Wilson**
Cybersecurity Intern — CodeAlpha
[LinkedIn](https://www.linkedin.com/in/your-profile) | [GitHub](https://github.com/your-username)

---

> *This project was completed as part of the CodeAlpha Cybersecurity Internship Program.*
