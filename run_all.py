"""Convenience entry point: python3 run_all.py  ==  python3 wave2/run_all.py"""
import os
import runpy
import sys

sys.argv[0] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wave2", "run_all.py")
runpy.run_path(sys.argv[0], run_name="__main__")
