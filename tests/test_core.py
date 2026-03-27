import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from core.deleter import delete_items
from core.scanner import scan


class TestCore(unittest.TestCase):
    def test_scan_finds_tmpclaude_files_and_dirs(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "tmpclaude-abc"))
            os.makedirs(os.path.join(root, "keep"))
            file_path = os.path.join(root, "tmpclaude-xyz")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("x")
            nested = os.path.join(root, "keep", "tmpclaude-nested")
            with open(nested, "w", encoding="utf-8") as f:
                f.write("y")

            items = scan(root)
            paths = {item.path for item in items}
            self.assertIn(file_path, paths)
            self.assertIn(nested, paths)
            self.assertTrue(any(p.endswith("tmpclaude-abc") for p in paths))
            self.assertEqual(len(items), 3)

    def test_delete_items_removes_files_and_dirs(self):
        with tempfile.TemporaryDirectory() as root:
            dir_path = os.path.join(root, "tmpclaude-dir")
            os.makedirs(dir_path)
            file_path = os.path.join(root, "tmpclaude-file")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("data")
            items = scan(root)
            result = delete_items(items)

            self.assertFalse(os.path.exists(dir_path))
            self.assertFalse(os.path.exists(file_path))
            self.assertEqual(result.failed_count, 0)
            self.assertEqual(result.deleted_count, 2)


if __name__ == "__main__":
    unittest.main()
