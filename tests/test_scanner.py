import pytest
from scanner.decoder import decode_barcode_data
import numpy as np

def test_decode_utf8_success():
    """Test standard UTF-8 decoding."""
    raw = b"12345678"
    assert decode_barcode_data(raw) == "12345678"

def test_decode_fallback_latin1():
    """Test fallback to latin-1 for non-utf8 bytes."""
    raw = b"\xff\xfe\x00\x00" # invalid utf-8
    result = decode_barcode_data(raw)
    assert isinstance(result, str)
    assert len(result) > 0

def test_decode_empty():
    """Test decoding empty bytes."""
    assert decode_barcode_data(b"") == ""
