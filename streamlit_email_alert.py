# import streamlit as st
# from main import load_data, engineer_features, detect_anomalies, compose_report, send_email

# # App settings
# st.set_page_config(page_title="Attendance Irregularity Detector", layout="wide")
# st.title("📊 Attendance Irregularity Detection & Email System")

# # Upload file
# uploaded_file = st.file_uploader("📂 Upload Attendance CSV", type=["csv"])

# # Load email settings from secrets.toml
# EMAIL = st.secrets["EMAIL"]
# EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
# SMTP_SERVER = st.secrets["SMTP_SERVER"]
# SMTP_PORT = st.secrets["SMTP_PORT"]
# ALERT_EMAIL = EMAIL  # Can be same or separate

# # Admin email input (recipient)
# #admin_email = st.text_input("📧 Enter Admin Email (recipient)", value=EMAIL)

# # Process the data
# if uploaded_file and st.button("🔍 Detect Anomalies"):
#     df = load_data(uploaded_file)
#     features = engineer_features(df)
#     anomalies = detect_anomalies(features)
#     report = compose_report(df, anomalies)

#     users = df[['ID', 'Name', 'Role']].drop_duplicates().set_index('ID')
#     display = anomalies.merge(users, left_index=True, right_index=True)

#     st.subheader("🚨 Detected Irregularities")
#     st.dataframe(display[['Name', 'Role', 'Attendance_Rate', 'Late_Count', 'Early_Leave_Count']])
#     st.text_area("📧 Email Preview", report, height=300)

#     if st.button("📬 Send Report to Admin"):
#         try:
#             send_email(
#                 to_address=ALERT_EMAIL,
#                 subject="Monthly Attendance Irregularity Report",
#                 message=report,
#                 sender=EMAIL,
#                 password=EMAIL_PASSWORD,
#                 smtp_host=SMTP_SERVER,
#                 smtp_port=SMTP_PORT
#             )
#             st.success(f"✅ Email sent successfully to {admin_email}")
#         except Exception as e:
#             st.error(f"❌ Failed to send email: {e}")

import streamlit as st
from main import load_data, engineer_features, detect_anomalies, compose_report, send_email

# App settings
st.set_page_config(page_title="Attendance Irregularity Detector", layout="wide")
st.title("📊 Attendance Irregularity Detection & Email System")

# Upload file
uploaded_file = st.file_uploader("📂 Upload Attendance CSV", type=["csv"])

# Load email settings from secrets.toml
try:
    EMAIL = st.secrets["EMAIL"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
    SMTP_SERVER = st.secrets["SMTP_SERVER"]
    SMTP_PORT = st.secrets["SMTP_PORT"]
except KeyError as e:
    st.error(f"Missing key in secrets.toml: {e}")
    st.stop()

# Use same email as recipient or allow input
ALERT_EMAIL = st.text_input("📧 Enter Recipient Email", value=EMAIL)

# Process the uploaded CSV
if uploaded_file and st.button("🔍 Detect Anomalies"):
    try:
        # Step 1: Load data
        df = load_data(uploaded_file)

        # Step 2: Feature Engineering
        features = engineer_features(df)

        # Step 3: Detect Anomalies
        anomalies = detect_anomalies(features)

        # Step 4: Compose Report
        report = compose_report(df, anomalies)

        # Step 5: Merge data for display
        users = df[['ID', 'Name', 'Role']].drop_duplicates().set_index('ID')
        display = anomalies.merge(users, left_index=True, right_index=True)

        # Show results
        st.subheader("🚨 Detected Irregularities")
        st.dataframe(display[['Name', 'Role', 'Attendance_Rate', 'Late_Count', 'Early_Leave_Count']])

        # Show email preview
        st.subheader("📧 Email Report Preview")
        st.text_area("Email Content", report, height=300)

        # Step 6: Email Sending
        if st.button("📬 Send Report to Admin"):
            st.info("📤 Sending email...")
            try:
                send_email(
                    to_address=ALERT_EMAIL,
                    subject="Monthly Attendance Irregularity Report",
                    message=report,
                    sender=EMAIL,
                    password=EMAIL_PASSWORD,
                    smtp_host=SMTP_SERVER,
                    smtp_port=SMTP_PORT
                )
                st.success(f"✅ Email sent successfully to {ALERT_EMAIL}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")

    except Exception as e:
        st.error(f"❌ Error processing the file: {e}")
