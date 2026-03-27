"""Directory scanner for tmpclaude-* items."""

from __future__ import annotations

import os
from typing import List

from core.models import Item


def scan(root_path: str, prefix: str = "tmpclaude-") -> List[Item]:
    items: List[Item] = []
    _scan_dir(root_path, prefix, items)
    return items


def _scan_dir(path: str, prefix: str, items: List[Item]) -> None:
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    name = entry.name
                    is_dir = entry.is_dir(follow_symlinks=False)
                    if name.startswith(prefix):
                        try:
                            stat = entry.stat(follow_symlinks=False)
                            size = stat.st_size
                            mtime = stat.st_mtime
                        except OSError:
                            size = 0
                            mtime = 0.0
                        items.append(Item(entry.path, is_dir, size, mtime))
                        continue
                    if is_dir:
                        _scan_dir(entry.path, prefix, items)
                except OSError:
                    continue
    except OSError:
        return
