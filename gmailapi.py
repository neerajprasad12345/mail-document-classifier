from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailApi:

    def __init__(self, credentials_file: str = None):
        """
        Constructor for a GmailApi object.

        :param credentials_file (str): path to credentials file.
        If None then resources/credentials.json is taken as the
        default path
        """

        if not credentials_file:
            credentials_file = os.path.join('resources', 'credentials.json')

        if not os.path.exists(credentials_file):
            raise Exception("Credentials file not available at %s" % credentials_file)

        # token_file stores the user's access and refresh tokens, and
        # is created automatically when the authorization flow completes
        # for the first time.

        token_file = os.path.join('resources', 'token.pickle')

        creds = None
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    def get_labels(self):
        """
        Creates a connection to Gmail using the service object and fetches
        all the labels available.
        :return: `list` of `str`
        """
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels

