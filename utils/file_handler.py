#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File operations for OSINT tool
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class FileHandler:
    """Handles file I/O for reports, exports, and configs."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(".")
        self.reports_dir = self.base_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def save_report(self, data: Dict[str, Any], filename: str) -> Path:
        """Save report as JSON."""
        path = self.reports_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def load_report(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load report from JSON."""
        path = self.reports_dir / filename
        if not path.exists():
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def export_results(self, results: List[Dict], format: str = "json") -> Path:
        """Export results to file."""
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"osint_export_{ts}.{format}"
        path = self.reports_dir / name
        with open(path, "w", encoding="utf-8") as f:
            if format == "json":
                json.dump(results, f, ensure_ascii=False, indent=2)
            else:
                for r in results:
                    f.write(str(r) + "\n")
        return path
