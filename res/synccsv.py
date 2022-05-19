import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1rn20U7MOQmzPerJcqyOEQM2RRXsWRhXWkK0Lz9ulVCE'
SAMPLE_RANGE_NAME = 'A1:AA2000'


def main():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'secret.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                      range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    df = pd.DataFrame(values_input[1:], columns=values_input[0])
    # 将df转换为csv文件
    df.to_csv('res/picture.csv', index=False, encoding='utf-8')


main()
