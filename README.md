# 📊 Attendance Irregularity Detection System

This project automates the detection of irregular attendance patterns using machine learning. It analyzes attendance data, flags anomalies like low attendance, late arrivals, or early leaves, and generates a detailed monthly report. The system optionally sends email alerts and provides a web-based interface using Streamlit.

---

## 📁 Project Structure

├── attendance_irregularity_dataset.csv # Sample attendance dataset
├── sample_attendance_realtime.csv # Realtime attendance input (optional)
├── main.py # Core logic (data processing, ML, report generation)
├── sample.py # Simple email test script using Gmail SMTP
├── streamlit_email_alert.py # Streamlit-based web UI for detection and emailing
├── monthly_attendance_report.txt # Example output report
└── README.md # Project documentation


---

## ⚙️ Features

- 📥 Upload attendance CSV
- 🧠 Detect anomalies using Isolation Forest
- 📝 Generate a detailed report (with emojis!)
- 📧 Send alerts via email
- 🌐 Web-based interface with Streamlit

---

## 🧠 How It Works

1. **Data Preprocessing**  
   Converts entry and exit times to proper datetime format.

2. **Feature Engineering**  
   Flags late entries, early leaves, and calculates attendance rate.

3. **Anomaly Detection**  
   Uses `IsolationForest` to detect users with irregular patterns.

4. **Report Generation**  
   Creates a readable, emoji-based report.

5. **Email Alerts** *(optional)*  
   Sends the report to a specified email address using Gmail SMTP.

---

## 🚀 Quick Start

### 🔧 Requirements

- Python 3.7+
- Required libraries:
  ```bash
  pip install pandas scikit-learn streamlit
##🌐 Run Web App (Streamlit)
streamlit run streamlit_email_alert.py

###.streamlit/secrets.toml
EMAIL = "youremail@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

##📌 Sample Output

👤 Student_14 (Student)
   • Attendance Rate: 0.78
   • Late Arrivals: 0
   • Early Leaves: 0



