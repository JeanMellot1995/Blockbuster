import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "donotreply.growth@gmail.com"  # Enter your address
receiver_email = "jean.mellot@choco.com"  # Enter receiver address
password = "Growth2021!"
message = """\
Subject: Hi there

This message is sent from Python."""

message = MIMEMultipart("alternative")
message["Subject"] = "New Google Description without Category!"
message["From"] = sender_email
message["To"] = receiver_email




context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)