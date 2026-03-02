#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU memory management
Reserved for future ML model inference (e.g. face detection, NLP)
"""

from typing import Optional, Dict, Any


class GPUManager:
    """Manages GPU resources for compute-heavy tasks."""

    def __init__(self):
        self._in_use = False
        self._device: Optional[str] = None

    @property
    def available(self) -> bool:
        """Check if GPU/CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def acquire(self, device: Optional[str] = None) -> bool:
        """Acquire GPU for use."""
        if self._in_use:
            return False
        self._in_use = True
        self._device = device or "cuda:0"
        return True

    def release(self) -> None:
        """Release GPU."""
        self._in_use = False
        self._device = None

    def get_info(self) -> Dict[str, Any]:
        """Get GPU info if available."""
        if not self.available:
            return {"available": False, "message": "CUDA not installed"}
        try:
            import torch
            return {
                "available": True,
                "device_count": torch.cuda.device_count(),
                "current_device": torch.cuda.current_device() if self._in_use else None,
            }
        except Exception as e:
            return {"available": False, "error": str(e)}
