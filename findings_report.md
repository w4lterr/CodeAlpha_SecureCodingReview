# Secure Code Review — Findings Report
### CodeAlpha Cybersecurity Internship — Task 3

**Target File:** `vulnerable_app.py`
**Language:** Python 3
**Reviewer:** Wilson
**Tool Used:** Bandit v1.9.4
**Scan Date:** 14 June 2026

---

## Summary

| Severity | Count |
|----------|-------|
| High | 3 |
| Medium | 4 |
| Low | 6 |
| **Total** | **13** |

---

## Findings

---

### [HIGH] B324 — Weak MD5 Hash for Password Storage
**Line:** 27
**CWE:** CWE-327 (Use of a Broken or Risky Cryptographic Algorithm)
**Code:**
```python
return hashlib.md5(password.encode()).hexdigest()
```
**Issue:**
MD5 is cryptographically broken and should never be used for password hashing. It is extremely fast to brute-force and entire precomputed rainbow tables exist online, making MD5-hashed passwords trivially crackable.

**Fix:**
```python
import bcrypt
return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

---

### [HIGH] B605 — Command Injection via os.system()
**Line:** 45
**CWE:** CWE-78 (OS Command Injection)
**Code:**
```python
os.system("ping -c 1 " + hostname)
```
**Issue:**
User-controlled input is passed directly to the shell. An attacker can inject additional commands using `;`, `&&`, or `|` (e.g. `hostname = "google.com; rm -rf /"`), executing arbitrary system commands.

**Fix:**
```python
import subprocess
subprocess.run(["ping", "-c", "1", hostname], shell=False)
```

---

### [HIGH] B602 — subprocess with shell=True
**Line:** 68
**CWE:** CWE-78 (OS Command Injection)
**Code:**
```python
output = subprocess.check_output("ls " + directory, shell=True)
```
**Issue:**
`shell=True` passes the full command string to the system shell, enabling command injection if the directory argument is user-controlled.

**Fix:**
```python
output = subprocess.check_output(["ls", directory], shell=False)
```

---

### [MEDIUM] B608 — SQL Injection via String Concatenation
**Line:** 36
**CWE:** CWE-89 (SQL Injection)
**Code:**
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)
```
**Issue:**
Concatenating user input directly into SQL queries allows attackers to manipulate the query structure. Input like `' OR '1'='1` returns all users; `'; DROP TABLE users; --` deletes the database entirely.

**Fix:**
```python
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

---

### [MEDIUM] B301 — Insecure Deserialization with pickle
**Line:** 53
**CWE:** CWE-502 (Deserialization of Untrusted Data)
**Code:**
```python
session = pickle.loads(f.read())
```
**Issue:**
`pickle.loads()` can execute arbitrary Python code embedded in a malicious payload. If the session file is attacker-controlled this is effectively remote code execution.

**Fix:**
```python
import json
with open(session_file, "r") as f:
    session = json.load(f)
```

---

### [MEDIUM] B307 — Use of eval()
**Line:** 61
**CWE:** CWE-78 (Code Injection)
**Code:**
```python
result = eval(expression)
```
**Issue:**
`eval()` executes any Python expression passed to it as a string. If user input reaches this function an attacker can run arbitrary code on the server.

**Fix:**
```python
import ast
result = ast.literal_eval(expression)
```

---

### [MEDIUM] B506 — yaml.load() Without Safe Loader
**Line:** 77
**CWE:** CWE-20 (Improper Input Validation)
**Code:**
```python
config = yaml.load(f)
```
**Issue:**
`yaml.load()` without a Loader argument can deserialize arbitrary Python objects, allowing code execution via a crafted YAML file.

**Fix:**
```python
config = yaml.safe_load(f)
```

---

### [LOW] B403 — Pickle Module Import
**Line:** 10
**CWE:** CWE-502 (Deserialization of Untrusted Data)
**Code:**
```python
import pickle
```
**Issue:**
Importing pickle signals reliance on an inherently unsafe serialization format. Any deserialization of untrusted data using pickle is dangerous.

**Fix:**
Replace pickle entirely with `json` or `msgpack` for data that may come from untrusted sources.

---

### [LOW] B404 — subprocess Module Import
**Line:** 13
**CWE:** CWE-78 (OS Command Injection)
**Code:**
```python
import subprocess
```
**Issue:**
subprocess can be used safely but requires careful usage. Always use `shell=False` and pass arguments as a list.

**Fix:**
Ensure all subprocess calls use `shell=False` and never concatenate user input into command strings.

---

### [LOW] B105 — Hardcoded Password: SECRET_KEY
**Line:** 19
**CWE:** CWE-259 (Use of Hard-coded Password)
**Code:**
```python
SECRET_KEY = "supersecretkey123"
```
**Issue:**
Hardcoded credentials in source code are exposed to anyone with repository access and will be committed to version control history permanently.

**Fix:**
```python
import os
SECRET_KEY = os.environ.get("SECRET_KEY")
```

---

### [LOW] B105 — Hardcoded Password: DB_PASSWORD
**Line:** 20
**CWE:** CWE-259 (Use of Hard-coded Password)
**Code:**
```python
DB_PASSWORD = "admin1234"
```
**Issue:**
Same as above — hardcoded database password exposed in source code.

**Fix:**
```python
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```

---

### [LOW] B101 — assert Used for Security Check
**Line:** 94
**CWE:** CWE-703 (Improper Check or Handling of Exceptional Conditions)
**Code:**
```python
assert is_admin, "Only admins can delete users"
```
**Issue:**
Python strips `assert` statements when run with the `-O` (optimise) flag, meaning this security check is completely bypassed in optimised builds.

**Fix:**
```python
if not is_admin:
    raise PermissionError("Only admins can delete users")
```

---

### [LOW] B311 — Insecure Random for Token Generation
**Line:** 106
**CWE:** CWE-330 (Use of Insufficiently Random Values)
**Code:**
```python
return str(random.randint(100000, 999999))
```
**Issue:**
Python's `random` module is not cryptographically secure and can be predicted. Tokens generated this way are unsuitable for authentication or session management.

**Fix:**
```python
import secrets
return str(secrets.randbelow(900000) + 100000)
```

---

## Overall Recommendations

1. **Never hardcode secrets** — use environment variables or a secrets manager
2. **Always use parameterised queries** — never concatenate user input into SQL
3. **Avoid shell=True** — always pass arguments as a list to subprocess
4. **Replace pickle** — use JSON for serialization of untrusted data
5. **Use bcrypt or argon2** for password hashing, never MD5 or SHA1
6. **Use yaml.safe_load()** — never yaml.load() on untrusted input
7. **Use the secrets module** for all security-sensitive random values
8. **Replace assert** with explicit if/raise for all security checks

---

> *This report was generated as part of the CodeAlpha Cybersecurity Internship — Task 3: Secure Coding Review.*
