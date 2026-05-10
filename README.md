ন

```markdown
# 🛡️ AI Exam Proctoring System

A real-time, AI-powered automated invigilation system designed to monitor online exams. This system leverages computer vision to detect behavioral violations and generates instant reports to ensure exam integrity.

---

## 📺 Project Demo
Check out the system in action:

![Proctoring Dashboard](Project%20Summary/Demo%20Screenshot/Screenshot%202026-05-10%20193320.png)

> **Watch the full video demonstration here:** [Demo Video Link](Project%20Summary/Demo.mp4/Demo%20video.mp4)

---

## ✨ Key Features
- **🤖 Intelligent Face Tracking**: Monitors student's gaze (Looking Left, Right, Up, or Away).
- **📱 Object Detection**: Real-time detection of prohibited items like mobile phones.
- **👥 Multi-Face Detection**: Flags an alert if more than one person is detected in the frame.
- **📸 Automatic Evidence Capture**: Saves screenshots of violations automatically with precise timestamps.
- **📊 Detailed Reporting**: Administrators can export violation logs in both **CSV** and **PDF** formats.
- **🖥️ Live Dashboard**: A clean, responsive web interface for seamless real-time monitoring.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Computer Vision**: OpenCV
- **AI Models**: YOLOv8 (Object Detection), Face Analysis logic
- **Database**: SQLite3
- **Reporting**: ReportLab (PDF), CSV Module
- **Frontend**: HTML5, CSS3, JavaScript

---

## 🚀 Getting Started

### Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nasim-dev0459/AI-Exam-Proctoring-System.git](https://github.com/nasim-dev0459/AI-Exam-Proctoring-System.git)
   cd AI-Exam-Proctoring-System

```

2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the application:**
```bash
python app.py

```


4. **Access the Dashboard:** Open your browser and go to `http://127.0.0.1:5000`

---

## 📂 Project Structure

* `app.py`: Main Flask application controller.
* `detector/`: Contains logic for face monitoring and object detection.
* `templates/`: HTML structures for the web dashboard.
* `static/`: Stores CSS, JS, and captured violation snapshots.
* `Project Summary/`: Contains demo screenshots, videos, and sample reports.

---

## 👤 Developed by

**MD Nasim Howladar** *Computer Science and Engineering Student* [GitHub Profile](https://github.com/nasim-dev0459)

