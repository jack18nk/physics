"""Render every math-ladder figure into output/.  Usage: python build.py [a b c]"""
import importlib
import sys
import time

MODULES = {"a": "ladder_a", "b": "ladder_b", "c": "ladder_c"}

if __name__ == "__main__":
    for key in sys.argv[1:] or MODULES:
        mod = importlib.import_module(MODULES[key])
        for name in sorted(n for n in dir(mod) if n.startswith("fig") and n[3:].isdigit()):
            t = time.time()
            getattr(mod, name)()
            print(f"  {name} ({time.time() - t:.1f}s)")
