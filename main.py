import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest
import smtplib
from email.mime.text import MIMEText

# def load_data(file_path):
#     df = pd.read_csv(file_path, parse_dates=['Date'])
#     df['Entry_Time'] = pd.to_datetime(df['Entry_Time'], errors='coerce').dt.time
#     df['Exit_Time'] = pd.to_datetime(df['Exit_Time'], errors='coerce').dt.time
#     return df

# def engineer_features(df):
#     df['Present_Flag'] = df['Status'] == 'Present'
#     df['Late_Flag'] = df['Entry_Time'].apply(lambda x: x is not None and x > datetime.strptime("09:15", "%H:%M").time())
#     df['Early_Leave_Flag'] = df['Exit_Time'].apply(lambda x: x is not None and x < datetime.strptime("15:45", "%H:%M").time())

#     return df.groupby('ID').agg({
#         'Present_Flag': 'mean',
#         'Late_Flag': 'sum',
#         'Early_Leave_Flag': 'sum'
#     }).rename(columns={
#         'Present_Flag': 'Attendance_Rate',
#         'Late_Flag': 'Late_Count',
#         'Early_Leave_Flag': 'Early_Leave_Count'
#     })

# def detect_anomalies(features):
#     model = IsolationForest(contamination=0.1, random_state=42)
#     features['Anomaly'] = model.fit_predict(features)
#     return features[features['Anomaly'] == -1]

# def compose_report(df, anomalies):
#     users = df[['ID', 'Name', 'Role']].drop_duplicates().set_index('ID')
#     report = anomalies.merge(users, left_index=True, right_index=True)
#     message = "Monthly Attendance Irregularity Report:\n\n"
#     for _, row in report.iterrows():
#         message += f"{row['Name']} ({row['Role']})\n"
#         message += f" - Attendance Rate: {row['Attendance_Rate']:.2f}\n"
#         message += f" - Late Arrivals: {row['Late_Count']}\n"
#         message += f" - Early Leaves: {row['Early_Leave_Count']}\n\n"
#     return message

# def send_email(to_address, subject, message, sender, password, smtp_host, smtp_port):
#     msg = MIMEText(message)
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = to_address
#     with smtplib.SMTP(smtp_host, smtp_port) as server:
#         server.starttls()
#         server.login(sender, password)
#         server.send_message(msg)

import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import smtplib
from email.mime.text import MIMEText

# Load dataset and convert time columns
def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df['Entry_Time'] = pd.to_datetime(df['Entry_Time'], format="%H:%M", errors='coerce').dt.time
    df['Exit_Time'] = pd.to_datetime(df['Exit_Time'], format="%H:%M", errors='coerce').dt.time
    return df

# Engineer attendance features
def engineer_features(df):
    df['Present_Flag'] = df['Status'] == 'Present'
    df['Late_Flag'] = df['Entry_Time'].apply(
        lambda x: pd.notnull(x) and x > datetime.strptime("09:15", "%H:%M").time()
    )
    df['Early_Leave_Flag'] = df['Exit_Time'].apply(
        lambda x: pd.notnull(x) and x < datetime.strptime("15:45", "%H:%M").time()
    )

    return df.groupby('ID').agg({
        'Present_Flag': 'mean',
        'Late_Flag': 'sum',
        'Early_Leave_Flag': 'sum'
    }).rename(columns={
        'Present_Flag': 'Attendance_Rate',
        'Late_Flag': 'Late_Count',
        'Early_Leave_Flag': 'Early_Leave_Count'
    })

# Detect anomalies in attendance patterns
def detect_anomalies(features):
    model = IsolationForest(contamination=0.1, random_state=42)
    features['Anomaly'] = model.fit_predict(features)
    return features[features['Anomaly'] == -1]

# Create a readable report
def compose_report(df, anomalies):
    users = df[['ID', 'Name', 'Role']].drop_duplicates().set_index('ID')
    report = anomalies.merge(users, left_index=True, right_index=True)
    message = "📢 Monthly Attendance Irregularity Report:\n\n"
    for _, row in report.iterrows():
        message += f"👤 {row['Name']} ({row['Role']})\n"
        message += f"   • Attendance Rate: {row['Attendance_Rate']:.2f}\n"
        message += f"   • Late Arrivals: {row['Late_Count']}\n"
        message += f"   • Early Leaves: {row['Early_Leave_Count']}\n\n"
    return message

# Send the report via email (optional)
def send_email(to_address, subject, message, sender, password, smtp_host, smtp_port):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_address
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

# Main function
def main():
    file_path = "attendance_irregularity_dataset.csv"  # Ensure this file exists in the same folder
    df = load_data(file_path)
    features = engineer_features(df)
    anomalies = detect_anomalies(features)

    if not anomalies.empty:
        report = compose_report(df, anomalies)
        print(report)

        # ✅ Save report with UTF-8 encoding to support emojis
        with open("monthly_attendance_report.txt", "w", encoding="utf-8") as f:
            f.write(report)

        # ✅ Optional: Send report via email
        # send_email(
        #     to_address="recipient@example.com",
        #     subject="Monthly Attendance Irregularity Report",
        #     message=report,
        #     sender="youremail@gmail.com",
        #     password="your_app_password",
        #     smtp_host="smtp.gmail.com",
        #     smtp_port=587
        # )

    else:
        print("✅ No anomalies detected this month.")

if __name__ == "__main__":
    main()
