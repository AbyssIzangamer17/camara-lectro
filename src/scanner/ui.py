import cv2
import numpy as np
import time
from typing import List, Dict, Any

def draw_professional_feedback(
    frame: np.ndarray, 
    results: List[Dict[str, Any]], 
    session_history: List[Dict[str, Any]] = None,
    pending_scans: Dict[str, float] = None
) -> np.ndarray:
    """
    Draws a premium RED HUD overlay on the frame (@ui-ux-designer).
    Includes stability verification states and quantity tracking.
    """
    h, w, _ = frame.shape
    RED_TONE = (50, 50, 220) 
    YELLOW_TONE = (50, 200, 220) 
    
    # 1. Create Glassmorphic Sidebar (Right side)
    sidebar_width = 300
    overlay = frame.copy()
    cv2.rectangle(overlay, (w - sidebar_width, 0), (w, h), (20, 20, 40), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    
    # Aesthetic Symbol |-/ in top-left
    cv2.putText(frame, "|-/", (20, 40), 
                cv2.FONT_HERSHEY_DUPLEX, 1.2, RED_TONE, 2, cv2.LINE_AA)

    # Sidebar Header
    cv2.putText(frame, "SCAN HISTORY", (w - sidebar_width + 20, 40), 
                cv2.FONT_HERSHEY_DUPLEX, 0.7, RED_TONE, 1, cv2.LINE_AA)
    cv2.line(frame, (w - sidebar_width + 20, 55), (w - 20, 55), (60, 60, 150), 1)

    # 2. List History (Product + Barcode + Quantity)
    if session_history:
        y_pos = 90
        # History is kept in order, but we display the count
        for i, entry in enumerate(session_history[-8:][::-1]):
            product = entry['product']
            barcode = entry['data']
            count = entry.get('count', 1)
            
            is_recent = (i == 0)
            text_color = (255, 255, 255) if is_recent else (200, 200, 200)
            code_color = RED_TONE if is_recent else (100, 100, 150)
            
            # Product Name with (x[Qty])
            qty_label = f" (x{count})" if count > 1 else ""
            display_name = f"{product}{qty_label}"
            if len(display_name) > 28:
                display_name = display_name[:25] + ".."
                
            cv2.putText(frame, display_name, (w - sidebar_width + 20, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
            
            cv2.putText(frame, f"ID: {barcode}", (w - sidebar_width + 20, y_pos + 18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, code_color, 1, cv2.LINE_AA)
            y_pos += 45

    # 3. Barcode Targets
    current_time = time.time()
    for res in results:
        data = res['data']
        product = res['product']
        rect = res['rect']
        polygon = res['polygon']
        
        status_color = RED_TONE
        label_prefix = ""
        
        if pending_scans and data in pending_scans:
            status_color = YELLOW_TONE
            progress = int((current_time - pending_scans[data]) * 100)
            label_prefix = f"[{min(progress, 99)}%] "
        
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, status_color, 2, cv2.LINE_AA)
        
        x, y, rw, rh = rect.left, rect.top, rect.width, rect.height
        c_len = 20
        for px, py in [(x, y), (x + rw, y), (x, y + rh), (x + rw, y + rh)]:
            sign_x = 1 if px == x else -1
            sign_y = 1 if py == y else -1
            cv2.line(frame, (px, py), (px + sign_x * c_len, py), status_color, 2)
            cv2.line(frame, (px, py), (px, py + sign_y * c_len), status_color, 2)
        
        label_text = f"{label_prefix}{product.upper()}"
        (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)
        lx, ly = x + (rw // 2) - (tw // 2), y - 20
        
        cv2.rectangle(frame, (lx - 5, ly - th - 5), (lx + tw + 5, ly + 5), status_color, -1)
        cv2.putText(frame, label_text, (lx, ly), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0) if status_color == YELLOW_TONE else (255, 255, 255), 1, cv2.LINE_AA)

    # 4. Global Status
    status_msg = "STATUS: TRACKING"
    if pending_scans:
        status_msg = "STATUS: VERIFYING..."
    cv2.putText(frame, status_msg, (20, h - 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED_TONE, 1, cv2.LINE_AA)

    return frame
