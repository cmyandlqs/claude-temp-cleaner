"""Deletion logic for tmpclaude-* items."""

from __future__ import annotations

import os
import shutil
import time
from typing import List

from core.models import DeleteResult, Item


def delete_items(items: List[Item]) -> DeleteResult:
    start = time.perf_counter()
    deleted = 0
    failed: List[Item] = []
    total_bytes = 0

    for item in items:
        try:
            if item.is_dir:
                shutil.rmtree(item.path)
            else:
                os.remove(item.path)
            deleted += 1
            total_bytes += item.size_bytes
        except OSError:
            failed.append(item)

    elapsed = time.perf_counter() - start
    return DeleteResult(
        deleted_count=deleted,
        failed_count=len(failed),
        failed_items=failed,
        total_bytes=total_bytes,
        elapsed_sec=elapsed,
    )
