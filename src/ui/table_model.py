"""Table model for scan results."""

from __future__ import annotations

from typing import List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from core.formatters import format_bytes, format_mtime
from core.models import Item


class ResultTableModel(QAbstractTableModel):
    headers = ["Path", "Type", "Size", "Modified"]

    def __init__(self, items: List[Item] | None = None) -> None:
        super().__init__()
        self._items: List[Item] = items or []

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return len(self._items)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return len(self.headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):  # noqa: ANN001
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        item = self._items[index.row()]
        col = index.column()
        if col == 0:
            return item.path
        if col == 1:
            return "Dir" if item.is_dir else "File"
        if col == 2:
            return format_bytes(item.size_bytes)
        if col == 3:
            return format_mtime(item.mtime)
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):  # noqa: ANN001,E501
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def set_items(self, items: List[Item]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def items(self) -> List[Item]:
        return list(self._items)
