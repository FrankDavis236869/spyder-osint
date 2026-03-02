#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Query Processing Pipeline
"""

from typing import Dict, Any, Optional

from .validator import Validator
from .inpainting import InpaintingEngine
from detection.detector import DataTypeDetector
from utils.logger import get_logger

logger = get_logger(__name__)


class Processor:
    """Main processing pipeline for OSINT queries."""

    def __init__(self):
        self.validator = Validator()
        self.inpainting = InpaintingEngine()
        self.detector = DataTypeDetector()

    def process(self, query: str, query_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Process an OSINT query through the full pipeline:
        1. Detect data type if not specified
        2. Validate input
        3. Execute lookup (placeholder)
        4. Enrich results
        """
        logger.info(f"Processing query: {query[:50]}...")

        # Auto-detect type if not given
        if not query_type:
            query_type = self.detector.detect(query)
            logger.debug(f"Detected type: {query_type}")

        # Validate
        is_valid, error = self.validator.validate(query, query_type)
        if not is_valid:
            logger.warning(f"Validation failed: {error}")
            return {"error": error, "valid": False}

        # Placeholder lookup - extend with actual API calls
        raw_result = self._lookup(query, query_type)

        # Enrich
        enriched = self.inpainting.enrich(query, query_type, raw_result)
        return enriched

    def _lookup(self, query: str, query_type: str) -> Dict[str, Any]:
        """Execute lookup based on query type. Extend with real APIs."""
        if query_type == "ip":
            return self._lookup_ip(query)
        if query_type == "email":
            return self._lookup_email(query)
        if query_type == "domain":
            return self._lookup_domain(query)
        if query_type == "phone":
            return self._lookup_phone(query)

        return {"query": query, "type": query_type, "status": "framework_ready"}

    def _lookup_ip(self, ip: str) -> Dict[str, Any]:
        import socket
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except (socket.gaierror, socket.herror):
            hostname = None
        return {"ip": ip, "hostname": hostname or "N/A"}

    def _lookup_email(self, email: str) -> Dict[str, Any]:
        return {"email": email, "valid_format": True}

    def _lookup_domain(self, domain: str) -> Dict[str, Any]:
        import socket
        try:
            ip = socket.gethostbyname(domain)
        except socket.gaierror:
            ip = None
        return {"domain": domain, "ip": ip or "N/A"}

    def _lookup_phone(self, phone: str) -> Dict[str, Any]:
        return {"phone": phone, "status": "framework_ready"}
