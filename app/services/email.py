import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Util:
    @staticmethod
    def send_email(data: dict):
        sender_email = "youremail@example.com"
        receiver_email = data['to_email']
        password = "yourpassword"

        message = MIMEMultipart("alternative")
        message["Subject"] = data['email_subject']
        message["From"] = sender_email
        message["To"] = receiver_email

        part = MIMEText(data['email_body'], "html")
        message.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
