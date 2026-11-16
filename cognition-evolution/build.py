"""Render every figure into output/.  Usage: python build.py [a b c d]"""
import importlib
import sys
import time

MODULES = {"a": "figs_a", "b": "figs_b", "c": "figs_c", "d": "figs_d"}

if __name__ == "__main__":
    for key in sys.argv[1:] or MODULES:
        mod = importlib.import_module(MODULES[key])
        for name in sorted(n for n in dir(mod) if n.startswith("fig") and n[3:].isdigit()):
            t = time.time()
            getattr(mod, name)()
            print(f"  {name} ({time.time() - t:.1f}s)")
