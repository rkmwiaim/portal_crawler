import json
import unittest
from pathlib import Path

import pydash

from definitions import TEST_RESOURCE_DIR, log
from external.spread_sheet_api import SpreadSheetApi

class SpreadsheetTest(unittest.TestCase):

    def setUp(self) -> None:
        test_config_path = Path(TEST_RESOURCE_DIR) / "config" / "test_config.json"
        with open(test_config_path) as f:
            spreadsheet_id = json.loads(f.read())['spreadsheet_id']
            self.spreadsheet_api = SpreadSheetApi(spreadsheet_id)

    def test_append(self):
        append_test_sheet_name = 'append_test'
        create_sheet_res = self.spreadsheet_api.create_sheet(append_test_sheet_name)
        sheet_id = pydash.get(create_sheet_res, 'replies.0.addSheet.properties.sheetId')
        log.info(f'append test sheet id: {sheet_id}')

        try:
            self.spreadsheet_api.append(f'{append_test_sheet_name}!B2', [['1', '2', '3']])
            self.spreadsheet_api.append(f'{append_test_sheet_name}!B2', [['4', '5', '6']])

            r1 = self.spreadsheet_api.get(f'{append_test_sheet_name}!B2:D2')
            r2 = self.spreadsheet_api.get(f'{append_test_sheet_name}!B3:D3')
            self.assertListEqual(r1, [['1', '2', '3']])
            self.assertListEqual(r2, [['4', '5', '6']])
        finally:
            self.spreadsheet_api.delete_sheet(sheet_id)
