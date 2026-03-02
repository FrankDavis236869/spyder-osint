#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Data Enrichment (Inpainting)
Assembles and enriches incomplete OSINT data by filling gaps
"""

from typing import Dict, Any, Optional


class InpaintingEngine:
    """Enriches OSINT queries by assembling data from multiple sources."""

    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def enrich(self, query: str, query_type: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich raw lookup data with additional context.
        Analogous to inpainting: fills gaps in the data profile.
        """
        enriched = raw_data.copy()
        enriched["query"] = query
        enriched["query_type"] = query_type

        # Add metadata
        enriched["_enriched"] = True
        enriched["_confidence"] = self._estimate_confidence(raw_data)

        return enriched

    def _estimate_confidence(self, data: Dict[str, Any]) -> float:
        """Estimate confidence score for the assembled data (0.0-1.0)."""
        if not data:
            return 0.0
        filled_fields = sum(1 for v in data.values() if v is not None and v != "")
        return min(1.0, filled_fields / 5)

    def merge_results(self, *sources: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple lookup results, preferring non-null values."""
        merged: Dict[str, Any] = {}
        for source in sources:
            for k, v in source.items():
                if k.startswith("_"):
                    continue
                if v and (k not in merged or not merged[k]):
                    merged[k] = v
        return merged
