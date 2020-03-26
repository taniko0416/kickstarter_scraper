import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
SHARED_DRIVE_FOLDER_ID = 'xxxxxxxxxxxx'

class GoogleSheets():
    def __init__(self, values):
        self.__auth()
        self.values = values
        self.service_sheet = build('sheets', 'v4', credentials=self.creds)

    def fillin(self):
        self.__create_sheet()
        request_body = {
            'valueInputOption': 'USER_ENTERED',
            'data': [
                {
                     'range': 'シート1!A2',
                     'majorDimension': 'COLUMNS',
                     'values': self.values 
                }
            ]
        }
        resp = self.service_sheet.spreadsheets().values().batchUpdate(spreadsheetId=self.ssid, body=request_body).execute()
        print(resp)
        return self.ssurl

    def __create_sheet(self):
        ### create spreadsheet
        ss = self.service_sheet.spreadsheets().create( body={ 'properties': { 'title': "Sample SS" } } ).execute()
        self.ssid = ss.get('spreadsheetId')
        self.ssurl = ss.get('spreadsheetUrl')
        ### mv to shared folder
        service_drive = build('drive', 'v3', credentials=self.creds)
        service_drive.files().update( fileId=self.ssid, addParents=SHARED_DRIVE_FOLDER_ID ).execute()

    def __auth(self):
        self.creds = None
        if os.path.exists('./config/token.pickle'):
            with open('./config/token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./config/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('./config/token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

# print( GoogleSheets( [[1,2,3],[1,2],[1,2,3]] ).fillin() )
