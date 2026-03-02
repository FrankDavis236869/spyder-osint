#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNN-style detection engine for OSINT data types
Classifies input string as phone, IP, email, domain, etc.
"""

import re
from typing import Optional

from .signature import SignatureAnalyzer
from .temporal import TemporalAnalyzer


class DataTypeDetector:
    """Detects OSINT query data type from raw input."""

    PATTERNS = {
        "ip": re.compile(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
            r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        ),
        "email": re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$"),
        "phone": re.compile(r"^\+?[\d\s\-\(\)]{10,20}$"),
        "domain": re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9\-\.]*\.[a-zA-Z]{2,}$"),
    }

    def __init__(self):
        self.signature = SignatureAnalyzer()
        self.temporal = TemporalAnalyzer()

    def detect(self, text: str) -> str:
        """
        Detect data type of input string.
        Returns: phone, ip, email, domain, username, name, address, or plate.
        """
        text = (text or "").strip()
        if not text:
            return "unknown"

        if self.PATTERNS["ip"].match(text):
            return "ip"
        if self.PATTERNS["email"].match(text):
            return "email"
        if self.PATTERNS["phone"].match(text):
            return "phone"
        if self.PATTERNS["domain"].match(text) and ".." not in text:
            return "domain"

        # Fallback: use signature heuristics
        return self.signature.classify(text)
