import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sheets import JST, SheetManager


class SheetManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = SheetManager.__new__(SheetManager)
        self.ws = MagicMock()
        self.manager._get_worksheet = MagicMock(return_value=self.ws)

    def test_normalize_date_accepts_hyphen(self):
        self.assertEqual(
            SheetManager._normalize_date("2026-08-09"),
            "2026/08/09",
        )

    @patch("sheets.datetime")
    def test_get_next_post_uses_jst_date(self, mock_datetime):
        now = MagicMock()
        now.strftime.return_value = "2026/08/09"
        mock_datetime.now.return_value = now

        self.ws.get_all_records.return_value = [
            {
                "投稿日": "2026/08/09",
                "時間帯": "morning",
                "投稿文": "おはようございます",
                "種別": "reassurance",
                "ネタID": "K001",
                "投稿済": "",
            }
        ]

        result = self.manager.get_next_post("投稿キュー", "morning")

        mock_datetime.now.assert_called_once_with(JST)
        self.assertIsNotNone(result)
        self.assertEqual(result["neta_id"], "K001")
        self.assertEqual(result["type"], "reassurance")

    @patch("sheets.datetime")
    def test_get_next_post_skips_other_day(self, mock_datetime):
        now = MagicMock()
        now.strftime.return_value = "2026/08/09"
        mock_datetime.now.return_value = now

        self.ws.get_all_records.return_value = [
            {
                "投稿日": "2026/08/08",
                "時間帯": "morning",
                "投稿文": "前日の投稿",
                "種別": "reassurance",
                "ネタID": "K000",
                "投稿済": "",
            }
        ]

        result = self.manager.get_next_post("投稿キュー", "morning")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
