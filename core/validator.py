#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input validation for OSINT queries
"""

import re
from typing import Tuple, Optional

VALID_TYPES = ("phone", "ip", "email", "domain", "username", "name", "address", "plate")


class Validator:
    """Validates OSINT query inputs."""

    IPV4_PATTERN = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    PHONE_PATTERN = re.compile(r"^\+?[\d\s\-\(\)]{10,20}$")
    DOMAIN_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9\-\.]*\.[a-zA-Z]{2,}$")

    def validate(self, query: str, query_type: str) -> Tuple[bool, Optional[str]]:
        """
        Validate query for given type.
        Returns (is_valid, error_message).
        """
        query = (query or "").strip()
        if not query:
            return False, "Query is empty"

        if query_type not in VALID_TYPES:
            return False, f"Invalid query type: {query_type}"

        if query_type == "ip":
            return self._validate_ip(query)
        if query_type == "email":
            return self._validate_email(query)
        if query_type == "phone":
            return self._validate_phone(query)
        if query_type == "domain":
            return self._validate_domain(query)
        if query_type in ("username", "name", "address", "plate"):
            return len(query) >= 2, None if len(query) >= 2 else "Input too short"

        return True, None

    def _validate_ip(self, s: str) -> Tuple[bool, Optional[str]]:
        if self.IPV4_PATTERN.match(s):
            return True, None
        return False, "Invalid IPv4 format"

    def _validate_email(self, s: str) -> Tuple[bool, Optional[str]]:
        if self.EMAIL_PATTERN.match(s):
            return True, None
        return False, "Invalid email format"

    def _validate_phone(self, s: str) -> Tuple[bool, Optional[str]]:
        if self.PHONE_PATTERN.match(s):
            return True, None
        return False, "Invalid phone format"

    def _validate_domain(self, s: str) -> Tuple[bool, Optional[str]]:
        if self.DOMAIN_PATTERN.match(s) and ".." not in s:
            return True, None
        return False, "Invalid domain format"
