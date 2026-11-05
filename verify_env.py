import sys
import pandas as pd
import numpy as np
import matplotlib
import sklearn
import streamlit as st
import IPython

print(f"PYTHON_VERSION: {sys.version.split()[0]}")
print(f"INTERPRETER_PATH: {sys.executable}")
print(f"PANDAS_VERSION: {pd.__version__}")
print(f"NUMPY_VERSION: {np.__version__}")
print(f"MATPLOTLIB_VERSION: {matplotlib.__version__}")
print(f"SKLEARN_VERSION: {sklearn.__version__}")
print(f"STREAMLIT_VERSION: {st.__version__}")
print(f"IPYTHON_VERSION: {IPython.__version__}")
print("ALL_IMPORTS_PASSED: True")
print("READY")
