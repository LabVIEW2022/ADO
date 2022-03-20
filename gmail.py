
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


email_sender_account = "ado@bellwethercoffee.com" #your email
email_sender_username = "ado@bellwethercoffee.com"  #your email username
email_sender_password = "anuocoqkxtvotzca"#your email password
email_smtp_server = "smtp.gmail.com" #change if not gmail.
email_smtp_port = 587 #change if needed.
email_recepients = ['rin@bellwethercoffee.com',
                    'helen@bellwethercoffee.com',
                    'eddie@bellwethercoffee.com',
                    'bharat@bellwethercoffee.com',
                    'theron@bellwethercoffee.com',
                    'lyumang@celestica.com',
                    'scott@bellwethercoffee.com'] #your receipts

class Mail:
    def __init__(self):
        pass
    def SendEmail (self, subject, body):
        email_subject = subject
        email_body = body
        server = smtplib.SMTP(email_smtp_server,email_smtp_port)
        print(f"Logging in to {email_sender_account}")
        server.starttls()
        server.login(email_sender_username, email_sender_password)
        for recipient in email_recepients:
            print(f"Sending email to {recipient}")
            message = MIMEMultipart('alternative')
            message['From'] = email_sender_account
            message['To'] = recipient
            message['Subject'] = email_subject
            message.attach(MIMEText(email_body, 'html'))
            server.sendmail(email_sender_account,recipient,message.as_string())
        server.quit()

mail = Mail()