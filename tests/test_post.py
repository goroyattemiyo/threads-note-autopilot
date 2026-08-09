import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import post


class PostClientTest(unittest.TestCase):
    @patch("post.SheetManager")
    @patch("post.ThreadsAPI")
    def test_build_clients_uses_generic_environment_variables(
        self,
        mock_threads_api,
        mock_sheet_manager,
    ):
        env = {
            "THREADS_ACCESS_TOKEN": "token",
            "THREADS_USER_ID": "user",
            "GOOGLE_SHEETS_CREDENTIALS": '{"type":"service_account"}',
            "SPREADSHEET_ID": "sheet-id",
        }

        with patch.dict(os.environ, env, clear=True):
            post.build_clients()

        mock_threads_api.assert_called_once_with("token", "user")
        mock_sheet_manager.assert_called_once_with(
            '{"type":"service_account"}',
            "sheet-id",
        )

    def test_load_env_exits_when_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                post.load_env("THREADS_ACCESS_TOKEN")


if __name__ == "__main__":
    unittest.main()
