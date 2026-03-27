"""Background workers for scan/delete."""

from __future__ import annotations

import time
from typing import List

from PySide6.QtCore import QObject, Signal

from core.deleter import delete_items
from core.models import DeleteResult, Item
from core.scanner import scan


class ScanWorker(QObject):
    started = Signal()
    finished = Signal(list, float)

    def __init__(self, path: str, prefix: str = "tmpclaude-") -> None:
        super().__init__()
        self._path = path
        self._prefix = prefix

    def run(self) -> None:
        self.started.emit()
        start = time.perf_counter()
        items = scan(self._path, self._prefix)
        elapsed = time.perf_counter() - start
        self.finished.emit(items, elapsed)


class DeleteWorker(QObject):
    started = Signal()
    finished = Signal(DeleteResult)

    def __init__(self, items: List[Item]) -> None:
        super().__init__()
        self._items = items

    def run(self) -> None:
        self.started.emit()
        result = delete_items(self._items)
        self.finished.emit(result)
