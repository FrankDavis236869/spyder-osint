#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder OSINT - Application entry point
"""

import sys

from gui.main_window import MainWindow
from utils import ensure_env


@ensure_env
def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
    sys.exit(0)
