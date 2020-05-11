from __future__ import print_function

import os.path
import pickle

from functional import seq
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

import definitions
import pydash


class SpreadSheetApi:
  def __init__(self, spreadsheet_id):
    self.service_account_file = os.path.join(definitions.RESOURCE_DIR, 'youtube-crawler-spreadsheet.json')
    self.spreadsheet_id = spreadsheet_id
    self.spreadsheet_resource = self.get_spreadsheet_resource()

  def get_spreadsheet_resource(self):
    """Shows basic usage of the Sheets API.
      Prints values from a sample spreadsheet.
      """
    token_path = os.path.join(definitions.RESOURCE_DIR, 'token.pickle')

    creds = None
    if os.path.exists(token_path):
      with open(token_path, 'rb') as token:
        creds = pickle.load(token)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        credentials = service_account.Credentials.from_service_account_file(
          self.service_account_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
      with open(token_path, 'wb') as token:
        pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    return service.spreadsheets()

  def get_sheets(self):
    spreadsheet_meta = self.spreadsheet_resource.get(spreadsheetId=self.spreadsheet_id).execute()
    sheets_seq = seq(spreadsheet_meta['sheets'])
    return sheets_seq.map(lambda d: d['properties'])

  def get_sheet_titles(self):
    spreadsheet_meta = self.spreadsheet_resource.get(spreadsheetId=self.spreadsheet_id).execute()
    sheets_seq = seq(spreadsheet_meta['sheets'])
    return sheets_seq.map(lambda d: d['properties']['title']).to_list()

  def add_sheet(self, sheet_name):
    update_body = {
      'requests': [
        {
          'addSheet': {
            'properties': {
              'title': sheet_name
            }
          }
        }
      ]
    }
    return self.spreadsheet_resource.batchUpdate(spreadsheetId=self.spreadsheet_id, body=update_body).execute()

  def get_sheet_id_from_response(self, add_sheet_response):
    return pydash.get(add_sheet_response, 'replies.0.addSheet.properties.sheetId')

  def get(self, range):
    get_result = self.spreadsheet_resource.values().batchGet(spreadsheetId=self.spreadsheet_id, ranges=range).execute()
    return pydash.get(get_result, 'valueRanges.0.values')

  def append(self, range, data):
    body = {
      "range": range,
      "majorDimension": "ROWS",
      "values": data,
    }
    return self.spreadsheet_resource.values()\
      .append(spreadsheetId=self.spreadsheet_id,
              valueInputOption='USER_ENTERED',
              insertDataOption='INSERT_ROWS',
              body=body,
              range=range
              )\
      .execute()

  def batch_append(self, sheet_id, data):
    rows = self.get_rows(data)

    body = {
      'requests': [
        {
          'appendCells':
            {
              "sheetId": sheet_id,
              "rows": rows,
              "fields": '*'
            }
        }
      ]
    }
    return self.spreadsheet_resource.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

  def get_rows(self, data):
    rows = []
    for row in data:
      rows.append(
        {
          'values':
            [
              {'userEnteredValue': {'stringValue': c}} for c in row
            ]
        }
      )
    return rows

if __name__ == '__main__':
  api = SpreadSheetApi('1se6gCkUgE6kajK_14jpVHPhOAbUt2dQ7aF74Oyw16KE')
  sheets = api.get_sheets()
  print(sheets)
