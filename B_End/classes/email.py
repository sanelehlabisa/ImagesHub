import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def __init__(self, sender_email_address: str, app_password: str) -> None:
        self.sender_email_address = sender_email_address
        self.app_password = app_password
        
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(self.sender_email_address, self.app_password)  
        self.server = server

    def send(self, receiver_email_address: str, subject: str, body: str) -> bool:
        message = MIMEMultipart()
        message['From'] = self.sender_email_address
        message['To'] = receiver_email_address
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            self.server.sendmail(self.sender_email_address, receiver_email_address, message.as_string())
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            self.server.quit()  

        return True


"""
if __name__ == "__main__":
    load_dotenv()
    sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
    app_password = os.getenv("SENDER_EMAIL_ADDRESS_APP_PASSWORD")
    
    receiver_email_address = os.getenv("RECEIVER_EMAIL_ADDRESS")
    subject = "Images Hub SMTP Email"
    body = "
    Hi

    We are hoping this email finds you well, we would like to let you know that guest has submitted a request for an image.

    Thanks

    Kind Regards
    Images Hub Team
    "

    email_obj = Email(sender_email_address, app_password)
    if email_obj.send(receiver_email_address, subject, body):
        print("Email sent successfully!")
    else:
        print("Email failed to send!")
"""