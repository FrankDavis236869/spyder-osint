#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Signature / pattern analysis for OSINT data
"""

import re
from typing import Optional


class SignatureAnalyzer:
    """Analyzes input signatures for classification."""

    PLATE_EU = re.compile(r"^[A-Z]{1,3}[\s\-]?[0-9]{1,4}[\s\-]?[A-Z]{1,3}$", re.I)
    PLATE_ASIA = re.compile(r"^[^\W_]{2,3}[\s\-]?[0-9]{2,4}[\s\-]?[^\W_]{1,4}$")

    def classify(self, text: str) -> str:
        """
        Classify text by signature heuristics.
        Returns: username, name, address, plate, or unknown.
        """
        text = text.strip()
        if len(text) < 2:
            return "unknown"

        # License plate patterns
        clean = re.sub(r"\s+", "", text)
        if self.PLATE_EU.match(clean) or self.PLATE_ASIA.match(clean):
            return "plate"

        # Username: alphanumeric, dots, underscores
        if re.match(r"^[\w\.\-]{3,32}$", text) and " " not in text:
            return "username"

        # Address: contains numbers and letters, possibly commas
        if re.search(r"\d", text) and re.search(r"[a-zA-Z]", text):
            return "address"

        # Name: typically words with spaces
        if " " in text and all(c.isalpha() or c in " .-" for c in text):
            return "name"

        return "username"
