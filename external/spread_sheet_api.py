from __future__ import print_function

import os.path

import pydash
from google.oauth2 import service_account
from googleapiclient.discovery import build

import definitions


class SpreadSheetApi:
  def __init__(self, spreadsheet_id):
    self.service_account_file = os.path.join(definitions.RESOURCE_DIR, 'youtube-crawler-spreadsheet.json')
    self.spreadsheet_id = spreadsheet_id
    self.spreadsheet_resource = self.get_spreadsheet_resource()

  def get_spreadsheet_resource(self):
    credentials = service_account.Credentials.from_service_account_file(
      self.service_account_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    return service.spreadsheets()

  def create_sheet(self, sheet_name):
    return self.batch_update([{'addSheet': {'properties': {'title': sheet_name}}}])

  def delete_sheet(self, sheet_id):
    return self.batch_update([{'deleteSheet': {'sheetId': sheet_id}}])

  def batch_update(self, requests):
    return self.spreadsheet_resource.batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                 body={'requests': requests}).execute()


  def get(self, range):
    get_result = self.spreadsheet_resource.values().batchGet(spreadsheetId=self.spreadsheet_id, ranges=range).execute()
    return pydash.get(get_result, 'valueRanges.0.values')

  def append(self, range, data):
    body = {
      "range": range,
      "majorDimension": "ROWS",
      "values": data,
    }
    return self.spreadsheet_resource.values() \
      .append(spreadsheetId=self.spreadsheet_id,
              valueInputOption='USER_ENTERED',
              insertDataOption='INSERT_ROWS',
              body=body,
              range=range
              ) \
      .execute()
