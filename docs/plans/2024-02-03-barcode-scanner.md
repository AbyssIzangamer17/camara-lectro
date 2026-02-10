# Real-Time Barcode Scanner Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a professional real-time barcode scanner using Python with asynchronous video capture, professional UI feedback, and Excel logging/automation features.

**Architecture:** Use `asyncio` for non-blocking video frame processing and UI updates. `opencv` handles camera input and display, `pyzbar` manages barcode detection. Records are stored in Excel or used for automated web searches.

**Tech Stack:** Python 3.12+, OpenCV, PyZbar, OpenPyXL, Playwright, UV (package manager).

---

### Task 1: Environment Setup
**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`

**Step 1: Initialize project with uv**
Run: `uv init .`
Expected: `pyproject.toml` and `.python-version` created.

**Step 2: Install dependencies**
Run: `uv add opencv-python pyzbar openpyxl playwright aiohttp`
Expected: Dependencies added to `pyproject.toml` and lockfile generated.

**Step 3: Setup Playwright**
Run: `uv run playwright install chromium`
Expected: Chromium browser installed for automation.

**Step 4: Commit**
Run: `git add . && git commit -m "chore: initial project setup with uv"`

---

### Task 2: Asynchronous Video Capture
**Files:**
- Create: `src/scanner/camera.py`
- Test: `tests/test_camera.py`

**Step 1: Write failing test for camera initialization**
```python
import pytest
from src.scanner.camera import AsyncCamera

@pytest.mark.asyncio
async def test_camera_init():
    cam = AsyncCamera()
    assert cam is not None
```

**Step 2: Implement AsyncCamera class (@async-python-patterns)**
```python
import cv2
import asyncio

class AsyncCamera:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
        self.running = False

    async def start(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open video device")
        self.running = True

    async def get_frame(self):
        if not self.running:
            return None
        loop = asyncio.get_event_loop()
        ret, frame = await loop.run_in_executor(None, self.cap.read)
        return frame if ret else None

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
```

**Step 3: Run tests**
Run: `uv run pytest tests/test_camera.py`
Expected: PASS

**Step 4: Commit**
Run: `git add src/scanner/camera.py tests/test_camera.py && git commit -m "feat: implement async camera capture"`

---

### Task 3: Decoding Logic (@ai-engineer)
**Files:**
- Create: `src/scanner/decoder.py`
- Test: `tests/test_decoder.py`

**Step 1: Write test for byte transformation**
```python
from src.scanner.decoder import decode_barcode_data
import pytest

def test_decode_utf8():
    raw_data = b"HELLO-123"
    assert decode_barcode_data(raw_data) == "HELLO-123"
```

**Step 2: Implement decoder with pyzbar**
```python
from pyzbar import pyzbar
import cv2

def decode_barcode_data(data: bytes) -> str:
    """Transform bytes to UTF-8 securely (@ai-engineer)."""
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('latin-1', errors='replace')

async def process_frame(frame):
    """Detect and decode barcodes in a frame."""
    barcodes = pyzbar.decode(frame)
    results = []
    for barcode in barcodes:
        data = decode_barcode_data(barcode.data)
        results.append({
            "data": data,
            "type": barcode.type,
            "rect": barcode.rect
        })
    return results
```

**Step 3: Run tests**
Run: `uv run pytest tests/test_decoder.py`
Expected: PASS

**Step 4: Commit**
Run: `git add src/scanner/decoder.py tests/test_decoder.py && git commit -m "feat: implement barcode decoding logic"`

---

### Task 4: Visual Feedback Design (@ui-ux-designer)
**Files:**
- Create: `src/scanner/ui.py`

**Step 1: Implement overlay drawer**
```python
import cv2

def draw_feedback(frame, results):
    """Draw professional visual feedback on the frame (@ui-ux-designer)."""
    for res in results:
        rect = res['rect']
        data = res['data']
        # Professional green box with rounded-like corners
        color = (0, 255, 0) # Modern Green
        x, y, w, h = rect.left, rect.top, rect.width, rect.height
        
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        
        # Draw label background
        cv2.rectangle(frame, (x, y - 30), (x + w, y), color, -1)
        cv2.putText(frame, data, (x + 5, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    return frame
```

**Step 2: Commit**
Run: `git add src/scanner/ui.py && git commit -m "feat: add professional UI feedback drawing"`

---

### Task 5: Integration & Automation (@xlsx-official / @browser-automation)
**Files:**
- Create: `src/scanner/exporter.py`
- Create: `src/main.py`

**Step 1: Implement Excel recording (@xlsx-official)**
```python
from openpyxl import Workbook, load_workbook
import os
from datetime import datetime

def log_to_excel(barcode_data, filename="scans.xlsx"):
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.append(["Timestamp", "Barcode Data"])
    else:
        wb = load_workbook(filename)
        ws = wb.active
    
    ws.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), barcode_data])
    wb.save(filename)
```

**Step 2: Implement main loop with async synchronization**
```python
import asyncio
import cv2
from src.scanner.camera import AsyncCamera
from src.scanner.decoder import process_frame
from src.scanner.ui import draw_feedback
from src.scanner.exporter import log_to_excel

async def main():
    cam = AsyncCamera()
    await cam.start()
    print("Scanner started. Press 'q' to quit.")
    
    last_scanned = set()
    
    try:
        while True:
            frame = await cam.get_frame()
            if frame is None:
                break
                
            results = await process_frame(frame)
            frame = draw_feedback(frame, results)
            
            for res in results:
                if res['data'] not in last_scanned:
                    print(f"Scanned: {res['data']}")
                    log_to_excel(res['data'])
                    last_scanned.add(res['data'])
            
            cv2.imshow("Professional Barcode Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            await asyncio.sleep(0.01)
    finally:
        cam.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
```

**Step 3: Commit**
Run: `git add src/scanner/exporter.py src/main.py && git commit -m "feat: integrate all components and add excel logging"`

---

### Task 6: Product Identification (@ai-engineer)
**Files:**
- Create: `src/scanner/products.py`
- Modify: `src/scanner/decoder.py`

**Step 1: Implement product lookup**
```python
# src/scanner/products.py
PRODUCT_DB = {
    "12345678": "Libreta Profesional",
    "87654321": "Crema de Manos Hidratante",
    "4005900114008": "Nivea Soft Cream",
    "UNKNOWN": "Producto No Identificado"
}

def get_product_name(barcode: str) -> str:
    return PRODUCT_DB.get(barcode, PRODUCT_DB["UNKNOWN"])
```

**Step 2: Update decoder to include product info**
```python
# Modify process_frame in src/scanner/decoder.py
from src.scanner.products import get_product_name

# inside loop...
        results.append({
            "data": data,
            "product": get_product_name(data),
            "type": barcode.type,
            "rect": barcode.rect
        })
```

**Step 3: Commit**
Run: `git add . && git commit -m "feat: add product identification database"`

---

### Task 7: Premium HUD UI Design (@ui-ux-designer)
**Files:**
- Modify: `src/scanner/ui.py`

**Step 1: Implement "Glassmorphic" HUD overlay**
```python
# src/scanner/ui.py
def draw_premium_hud(frame, results, last_scanned_list):
    # Add a semi-transparent dark sidebar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (250, frame.shape[0]), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Title
    cv2.putText(frame, "SCANNER PRO", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 127), 2)
    
    # List recent products in sidebar
    y_offset = 80
    for product in list(last_scanned_list)[-5:]:
        cv2.putText(frame, f"> {product}", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y_offset += 30
        
    # Draw refined targets over barcodes
    for res in results:
        # Drawing logic from Task 4 but with product name now
        ...
    return frame
```

**Step 2: Commit**
Run: `git add . && git commit -m "feat: upgrade UI to premium HUD design"`

