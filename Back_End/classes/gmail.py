import os
import webbrowser
import base64
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

TOKEN_FILE = './token.json'
CREDENTIALS_FILE = './credentials.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

class Gmail:
    def __init__(self, email_address: str) -> None:
        self.email_address: str = email_address
        self.credentials = self.get_credentials()
        if not self.credentials:
            self.credentials = self.authorize()
        print('Credentials initialized.')

    def authorize(self) -> Credentials:
        try:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            flow.redirect_uri = "https://oauth.pstmn.io/v1/browser-callback"
            authorization_url, _ = flow.authorization_url(access_type="offline", prompt="consent")

            webbrowser.open(authorization_url)
            print('A browser window should have opened for authorization. Please complete the authorization process.')

            authorization_response = input('Enter the full callback URL: ')
            flow.fetch_token(authorization_response=authorization_response)
            
            self.save_credentials(flow.credentials)
            print('Authorization successful.')
            return flow.credentials
        except Exception as e:
            print(f'Error during authorization: {e}')
            return None

    def save_credentials(self, credentials: Credentials) -> None:
        try:
            with open(TOKEN_FILE, 'w') as token_file:
                token_file.write(credentials.to_json())
        except Exception as e:
            print(f'Error saving credentials: {e}')

    def get_credentials(self) -> Credentials:
        try:
            if os.path.exists(TOKEN_FILE):
                credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                    self.save_credentials(credentials)
                elif credentials.expired:
                    print("Token expired and refresh token is not defined")
                    return None
                return credentials
            else:
                print("Token path does not exist")
                return None
        except Exception as e:
            print(f'Error loading credentials: {e}')
            return None

    def send(self, receiver_email_address: str, subject: str = 'New Guest Image Request for Images Hub') -> None:
        body = (
            "Hi there,\n\n"
            "We hope you are well.\n\n"
            "This is to notify you that a guest has submitted a request for access to an image.\n\n"
            "Please do not reply to this email.\n\n"
            "Thanks.\n\n"
            "Kind regards,\n"
            "Images Hub Team"
        )
        
        try:
            service = build('gmail', 'v1', credentials=self.credentials)
            message = {
                'raw': base64.urlsafe_b64encode(
                    f'To: {receiver_email_address}\r\nSubject: {subject}\r\n\r\n{body}'.encode('utf-8')
                ).decode('utf-8')
            }
            sent_message = service.users().messages().send(userId='me', body=message).execute()
            print(f'Message Id: {sent_message["id"]}')
        except Exception as err:
            print(f'This error "{err}" occurred while sending message')
"""
def main() -> None:
    load_dotenv()
    sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
    receiver_email_address = os.getenv("RECEIVER_EMAIL_ADDRESS")
    
    if not sender_email_address or not receiver_email_address:
        print("Error: Missing email addresses. Check environment variables.")
        return

    gmail = Gmail(sender_email_address)
    if gmail.credentials:
        gmail.send(receiver_email_address)
    else:
        print("Error: Authorization failed. Unable to send email.")

if __name__ == "__main__":
    main()
"""
