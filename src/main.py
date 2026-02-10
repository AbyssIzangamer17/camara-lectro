import asyncio
import cv2
import sys
import time
from scanner.camera import AsyncCamera
from scanner.decoder import process_frame
from scanner.ui import draw_professional_feedback
from scanner.exporter import log_to_excel

async def run_scanner():
    """
    Main application loop. Coordinates camera capture, decoding, 
    UI feedback, and data persistence with re-scan cooldown and quantity logic.
    """
    camera = AsyncCamera(camera_id=0)
    
    try:
        await camera.start()
        print("--- Real-Time Barcode Scanner ---")
        print("Status: Operation Active")
        print("Action: Press 'Q' to terminate session")
        print("Log: Barcodes require 1s of stability and 2s cooldown for re-scan.")
        
        # session_counts: {barcode: total_quantity}
        # last_verified_time: {barcode: timestamp} - to handle 2s cooldown
        session_counts = {}
        session_history = []
        last_verified_time = {}
        
        # Validation Buffer: {barcode: first_seen_timestamp}
        pending_scans = {}
        
        while True:
            # 1. Capture Frame (Async)
            frame = await camera.get_frame()
            if frame is None:
                print("Error: Failed to retrieve frame from camera.")
                break
                
            # 2. Process & Decode
            results = await process_frame(frame)
            current_time = time.time()
            detected_this_frame = set()
            
            # 3. Logic: Verification & Multi-scan with Cooldown
            for res in results:
                data = res['data']
                product = res['product']
                detected_this_frame.add(data)
                
                # Check for 2s cooldown if already scanned
                cooldown_active = False
                if data in last_verified_time:
                    if current_time - last_verified_time[data] < 2.0:
                        cooldown_active = True
                
                if cooldown_active:
                    continue

                # Start or update pending verification
                if data not in pending_scans:
                    pending_scans[data] = current_time
                else:
                    # Check if 1s stability is met
                    if current_time - pending_scans[data] >= 1.0:
                        # --- VERIFIED ---
                        print(f"[ACTION] {product} verified.")
                        log_to_excel(f"{product} [{data}]")
                        
                        # Update quantity
                        session_counts[data] = session_counts.get(data, 0) + 1
                        last_verified_time[data] = current_time
                        
                        # Update history
                        found = False
                        for entry in session_history:
                            if entry['data'] == data:
                                entry['count'] = session_counts[data]
                                found = True
                                break
                        if not found:
                            session_history.append({
                                "product": product,
                                "data": data,
                                "count": session_counts[data]
                            })
                        
                        # Sound PIP
                        try:
                            import winsound
                            loop = asyncio.get_event_loop()
                            loop.run_in_executor(None, winsound.Beep, 1000, 200)
                        except Exception:
                            pass
                            
                        # Remove from pending to allow cooldown to start
                        del pending_scans[data]

            # Cleanup pending: if barcode disappears, reset its stability timer
            for data in list(pending_scans.keys()):
                if data not in detected_this_frame:
                    del pending_scans[data]
            
            # 4. Professional Visual Feedback
            frame = draw_professional_feedback(frame, results, session_history, pending_scans)
            
            # 5. Display
            cv2.imshow("Scanner Feedback Interface", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(run_scanner())
