from pyzbar import pyzbar
import cv2
import numpy as np
from typing import List, Dict, Any

def decode_barcode_data(data: bytes) -> str:
    """
    Transforms bytes to a UTF-8 string.
    Falls back to latin-1 if UTF-8 fails to ensure robustness (@ai-engineer).
    """
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('latin-1', errors='replace')

from scanner.products import get_product_name

async def process_frame(frame: np.ndarray) -> List[Dict[str, Any]]:
    """
    Detects and decodes barcodes in a given image frame.
    Returns a list of dictionaries containing barcode data, type, and location.
    """
    if frame is None:
        return []

    # pyzbar.decode is a synchronous CPU-bound operation
    barcodes = pyzbar.decode(frame)
    
    results = []
    for barcode in barcodes:
        data = decode_barcode_data(barcode.data)
        results.append({
            "data": data,
            "product": get_product_name(data),
            "type": barcode.type,
            "rect": barcode.rect,
            "polygon": barcode.polygon
        })
    return results
