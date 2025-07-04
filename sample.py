import smtplib
from email.mime.text import MIMEText

EMAIL = "anshadali0101@gmail.com"
EMAIL_PASSWORD = "bugs mcuf jezs tirl"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

msg = MIMEText("Test email from Python")
msg["Subject"] = "Test Mail"
msg["From"] = EMAIL
msg["To"] = EMAIL  # send to yourself

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.sendmail(EMAIL, [EMAIL], msg.as_string())
    server.quit()
    print("✅ Email sent!")
except Exception as e:
    print("❌ Failed to send email:", e)
