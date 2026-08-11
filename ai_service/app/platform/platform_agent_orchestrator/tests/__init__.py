import os
import pytest

# Used to just ensure python resolves correctly
def pytest_configure(config):
    os.environ["PYTHONPATH"] = "."
