
import pytest
import ast
import os
from main import giveTimeStamp
from lint_engine import getDataLoadCount
from py_parser import checkLoggingPerData

def test_giveTimeStamp():
    # Test if giveTimeStamp returns a non-empty string
    timestamp = giveTimeStamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) > 0

def test_getDataLoadCount(tmp_path):
    # Create a temporary Python file with mock data load calls
    mock_file = tmp_path / "mock_script.py"
    mock_file.write_text("import torch\ntorch.load('data.pth')\n")
    
    # Test the getDataLoadCount function
    count = getDataLoadCount(str(mock_file))
    assert count == 1

def test_checkLoggingPerData():
    # Create a mock Python code snippet
    code = '''
import logging
def example_function():
    logging.info("Logging data load")
'''
    # Parse the code into an AST
    tree = ast.parse(code)
    
    # Test the checkLoggingPerData function
    result = checkLoggingPerData(tree, "data load")
    assert result is True
