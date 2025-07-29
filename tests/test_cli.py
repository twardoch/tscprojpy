# this_file: tscprojpy/tests/test_cli.py
"""Tests for the CLI module."""

import pytest
from tscprojpy.cli import hello, version


def test_hello_default(capsys):
    """Test hello function with default argument."""
    hello()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out


def test_hello_custom(capsys):
    """Test hello function with custom name."""
    hello("Python")
    captured = capsys.readouterr()
    assert "Hello, Python!" in captured.out


def test_version(capsys):
    """Test version function."""
    version()
    captured = capsys.readouterr()
    assert "tscprojpy" in captured.out