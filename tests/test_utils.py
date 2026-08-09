import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import utils


class UtilsSheetsClientTest(unittest.TestCase):
    @patch("utils.gspread.authorize")
    @patch("utils.google_auth_default")
    def test_get_sheets_client_uses_adc(self, mock_default, mock_authorize):
        credentials = MagicMock()
        client = MagicMock()
        spreadsheet = MagicMock()
        mock_default.return_value = (credentials, "project-id")
        mock_authorize.return_value = client
        client.open_by_key.return_value = spreadsheet

        with patch.dict(os.environ, {"SPREADSHEET_ID": "sheet-id"}, clear=True):
            result = utils.get_sheets_client()

        mock_default.assert_called_once_with(scopes=utils.SCOPES)
        mock_authorize.assert_called_once_with(credentials)
        client.open_by_key.assert_called_once_with("sheet-id")
        self.assertIs(result, spreadsheet)


if __name__ == "__main__":
    unittest.main()
