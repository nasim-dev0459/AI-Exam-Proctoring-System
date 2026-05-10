#Made with Nasim, BSc in CSE at ADUST 

import os
import cv2
import datetime
import sqlite3
import csv
from io import StringIO, BytesIO
from flask import Flask, render_template, Response, jsonify, send_file, make_response

# PDF generation library - Fixed import for Canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from detector.face_detector import ExamMonitor
from detector.object_detector import ObjectDetector

app = Flask(__name__)

# --- Setup Directories ---
CAPTURE_DIR = 'static/captures'
if not os.path.exists(CAPTURE_DIR):
    os.makedirs(CAPTURE_DIR)

# --- Initialize SQLite Database ---
def init_db():
    """Creates the violation log table if it doesn't exist."""
    conn = sqlite3.connect('exam_logs.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS violations 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       timestamp TEXT, 
                       event TEXT, 
                       image_path TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Initialize Models and Camera ---
face_monitor = ExamMonitor()
obj_detector = ObjectDetector()
camera = cv2.VideoCapture(0)

def log_violation_to_db(event_name, frame):
    """Logs violation details to the database and saves a snapshot."""
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_id = datetime.datetime.now().strftime("%H%M%S")
    image_name = f"alert_{file_id}.jpg"
    image_path = os.path.join(CAPTURE_DIR, image_name)
    
    # Save the current frame as evidence
    cv2.imwrite(image_path, frame)
    
    conn = sqlite3.connect('exam_logs.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO violations (timestamp, event, image_path) VALUES (?, ?, ?)",
                   (timestamp_str, event_name, image_name))
    conn.commit()
    conn.close()

def generate_frames():
    """Continuously captures frames and performs AI analysis."""
    last_log_time = datetime.datetime.now()
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Analyze frame for face and object (phone) detection
        face_count, face_status = face_monitor.analyze_frame(frame)
        phone_detected = obj_detector.detect_phone(frame) 
        
        final_status = face_status
        is_violation = False
        
        # Determine violation priority
        if phone_detected:
            final_status = "CHEATING: Phone Detected!"
            is_violation = True
        elif face_count > 1:
            final_status = "WARNING: Multiple Faces!"
            is_violation = True
        elif face_count == 0:
            final_status = "ALERT: Student Not Visible"
            is_violation = True
        elif "Looking" in face_status:
            is_violation = True

        # Capture evidence every 5 seconds if a violation is persistent
        current_time = datetime.datetime.now()
        if is_violation and (current_time - last_log_time).total_seconds() > 5:
            log_violation_to_db(final_status, frame)
            last_log_time = current_time
#Made with Nasim, BSc in CSE at ADUST 

        # Draw On-Screen Display (OSD)
        color = (0, 0, 255) if is_violation else (0, 255, 0) # Red for alert, Green for focused
        cv2.rectangle(frame, (0, 0), (500, 60), (0, 0, 0), -1)
        cv2.putText(frame, f"STATUS: {final_status}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Encode frame for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- Web Routes ---

@app.route('/')
def index():
    """Main Dashboard Page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Route for the live proctoring stream."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_logs')
def get_logs():
    """Fetch the latest 10 violation logs for the UI."""
    conn = sqlite3.connect('exam_logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM violations ORDER BY id DESC LIMIT 10")
    logs = cursor.fetchall()
    conn.close()
    return jsonify(logs)

@app.route('/get_stats')
def get_stats():
    """Fetch summary statistics for dashboard counters."""
    conn = sqlite3.connect('exam_logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM violations")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM violations WHERE event LIKE '%Phone%'")
    phones = cursor.fetchone()[0]
    conn.close()
    return jsonify({"total": total, "phones": phones})

@app.route('/export/csv')
def export_csv():
    """Generates and triggers download of a CSV report."""
    conn = sqlite3.connect('exam_logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, event FROM violations")
    rows = cursor.fetchall()
    conn.close()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Timestamp', 'Violation Type'])
    cw.writerows(rows)
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=exam_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/export/pdf')
def export_pdf():
    """Generates and triggers download of a PDF report using ReportLab."""
    conn = sqlite3.connect('exam_logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, event FROM violations")
    rows = cursor.fetchall()
    conn.close()
    
    buffer = BytesIO()
    # Initialize Canvas with the buffer
    p = Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "AI Exam Proctoring - Violation Report")
    
    p.setFont("Helvetica", 11)
    y = 710
    for row in rows:
        p.drawString(100, y, f"[{row[0]}] - {row[1]}")
        y -= 20
        # Create a new page if the current one is full
        if y < 50: 
            p.showPage()
            y = 750
            
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="exam_report.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    # use_reloader=False is used to prevent camera initialization twice
    app.run(debug=True, use_reloader=False)
    #Made with Nasim, BSc in CSE at ADUST 
