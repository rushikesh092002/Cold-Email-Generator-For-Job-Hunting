import smtplib
import os
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.config import EMAIL_SENDER , EMAIL_PASSWORD


def send_email(receiver_email,subject,body,attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if attachment_path:
            with open(attachment_path,"rb") as attachment:
                part = MIMEBase("application" ,"octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition",f"attachment; filename={os.path.basename(attachment_path)}")
                msg.attach(part)

            with smtplib.SMTP_SSL("smtp.gmail.com" , 465) as smtp:
                smtp.login(EMAIL_SENDER , EMAIL_PASSWORD)
                smtp.sendmail(EMAIL_SENDER ,receiver_email , msg.as_string())

                print("✅ Email sent successfully!")
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication Error: {e}")
        print("➡️ Ensure you are using the correct App Password.")