#!/usr/bin/env python3
import sys
from pathlib import Path

# Evil path fuckery
file = Path(__file__)
parent_dir = file.parent.parent
sys.path.append(str(parent_dir))


from src import run

run()
