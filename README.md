# 🛡️ AI Exam Proctoring System

A real-time, AI-powered automated invigilation system designed to monitor online exams. This system uses computer vision to detect behavioral violations and generates instant reports to ensure exam integrity.

---

## 📺 Project Demo
Check out the system in action:

![Proctoring Dashboard](Project%20Summary/Demo%20Screenshot/Screenshot%202026-05-10%20193320.png)

> **Watch the full video demonstration here:** [Demo Video Link](Project%20Summary/Demo.mp4/Demo%20video.mp4)

---

## ✨ Key Features
- **🤖 Intelligent Face Tracking**: Monitors student's gaze (Looking Left, Right, Up, or Away).
- **📱 Object Detection**: Detects prohibited items like mobile phones during the session.
- **👥 Multi-Face Detection**: Flags an alert if more than one person is visible in the frame.
- **📸 Automatic Evidence Capture**: Automatically saves screenshots of violations with timestamps.
- **📊 Detailed Reporting**: Admin can download violation logs in both **CSV** and **PDF** formats.
- **🖥️ Live Dashboard**: A clean, responsive web interface for real-time monitoring.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Computer Vision**: OpenCV
- **AI Models**: YOLOv8 (Object Detection), MediaPipe/Dlib (Face Analysis)
- **Database**: SQLite3
- **Reports**: ReportLab (PDF), CSV Module
- **Frontend**: HTML5, CSS3 (Bootstrap/Custom), JavaScript

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nasim-dev0459/AI-Exam-Proctoring-System.git](https://github.com/nasim-dev0459/AI-Exam-Proctoring-System.git)
   cd AI-Exam-Proctoring-System

  - Install dependencies:
  - pip install -r requirements.txt

   
  - Run the application:
  - python app.py
  - Project Structure
app.py: Main Flask application.

detector/: Contains logic for face and object detection.

templates/: HTML files for the web interface.

static/: CSS, JS, and captured violation images.

Project Summary/: Contains demo screenshots, video, and sample reports.


Developed by
MD Nasim Howladar Computer Science and Engineering Student
