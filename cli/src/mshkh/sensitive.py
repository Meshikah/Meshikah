"""Default sensitive-data patterns (library DEC-009). Findings never include the matched value."""

from __future__ import annotations

import re

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    "API key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "credential assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+]{12,}"),
    "connection string with password": re.compile(r"(?i)\b[a-z][a-z0-9+]*://[^\s:/@]+:[^\s@/]+@"),
}

PERSONAL_PATTERNS = {
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone number": re.compile(r"(?<![\w-])(?:\+\d{1,3}[\s.-]?)?\(?\d{2,3}\)?[\s.-]\d{3,4}[\s.-]\d{4}(?![\w-])"),
    "CURP": re.compile(r"\b[A-Z][AEIOUX][A-Z]{2}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b"),
    "RFC": re.compile(r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b"),
    "IBAN": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
}

DIGIT_RUN = re.compile(r"(?<![\w-])(?:\d[ -]?){13,19}(?![\w-])")
ALLOWED_EMAIL_SUFFIXES = ("@example.com", "@example.org", "@users.noreply.github.com")


def _luhn(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def scan_line(line: str) -> list[str]:
    """Return the names of the patterns found in one line."""
    found = [name for name, rx in SECRET_PATTERNS.items() if rx.search(line)]
    for name, rx in PERSONAL_PATTERNS.items():
        for match in rx.finditer(line):
            if name == "email address" and match.group(0).lower().endswith(ALLOWED_EMAIL_SUFFIXES):
                continue
            found.append(name)
            break
    for match in DIGIT_RUN.finditer(line):
        digits = re.sub(r"\D", "", match.group(0))
        if len(digits) == 18:
            found.append("CLABE")
            break
        if _luhn(digits):
            found.append("payment card number")
            break
    return found
