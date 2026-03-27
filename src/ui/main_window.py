"""Main window UI and interactions."""

from __future__ import annotations

import os
from typing import List

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from core.formatters import format_bytes
from core.models import Item
from ui.styles import STYLE_SHEET
from ui.table_model import ResultTableModel
from ui.workers import DeleteWorker, ScanWorker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Claude Temp Cleaner")
        self.resize(980, 640)

        QApplication.instance().setStyleSheet(STYLE_SHEET)

        self._items: List[Item] = []
        self._scan_thread: QThread | None = None
        self._scan_worker: ScanWorker | None = None
        self._delete_thread: QThread | None = None
        self._delete_worker: DeleteWorker | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(12)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Claude Temp Cleaner")
        title.setObjectName("Title")
        header_layout.addWidget(title)
        header_layout.addStretch(1)

        self.choose_button = QPushButton("Choose Folder")
        self.choose_button.setObjectName("Primary")
        self.choose_button.clicked.connect(self.on_choose_folder)
        header_layout.addWidget(self.choose_button)

        root_layout.addWidget(header)

        card = QWidget()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        self.status_label = QLabel("Select a folder to scan for tmpclaude-* items.")
        self.status_label.setObjectName("Muted")
        card_layout.addWidget(self.status_label)

        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.model = ResultTableModel([])
        self.table.setModel(self.model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(False)
        card_layout.addWidget(self.table)

        root_layout.addWidget(card, 1)

        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        self.stats_label = QLabel("No results yet")
        self.stats_label.setObjectName("Stats")
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch(1)

        self.delete_button = QPushButton("Delete All")
        self.delete_button.setObjectName("Danger")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        footer_layout.addWidget(self.delete_button)

        root_layout.addWidget(footer)

        self.setCentralWidget(root)

    def on_choose_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not path:
            return
        if not os.path.isdir(path):
            QMessageBox.warning(self, "Invalid Folder", "Selected path is not a folder.")
            return
        self._start_scan(path)

    def _start_scan(self, path: str) -> None:
        self._set_busy(True, "Scanning...")
        self._items = []
        self.model.set_items([])
        self.stats_label.setText("Scanning...")

        worker = ScanWorker(path)
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.started.connect(lambda: self.status_label.setText(f"Scanning: {path}"))
        worker.finished.connect(self._on_scan_finished)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self._scan_worker = worker
        self._scan_thread = thread
        thread.start()

    def _on_scan_finished(self, items: list, elapsed: float) -> None:
        self._items = list(items)
        self.model.set_items(self._items)
        self._scan_worker = None
        total_bytes = sum(item.size_bytes for item in self._items)
        self.stats_label.setText(
            f"Found {len(self._items)} items · {format_bytes(total_bytes)} · {elapsed:.2f}s"
        )
        if self._items:
            self.status_label.setText("Scan complete. Review items before deleting.")
        else:
            self.status_label.setText("No tmpclaude-* items found.")
        self._set_busy(False)

    def on_delete_clicked(self) -> None:
        if not self._items:
            return
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete {len(self._items)} items? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        self._start_delete()

    def _start_delete(self) -> None:
        self._set_busy(True, "Deleting...")
        worker = DeleteWorker(self._items)
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._on_delete_finished)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self._delete_worker = worker
        self._delete_thread = thread
        thread.start()

    def _on_delete_finished(self, result) -> None:  # DeleteResult
        self._items = []
        self.model.set_items([])
        self._delete_worker = None
        self._set_busy(False)
        if result.failed_count == 0:
            self.status_label.setText("Delete complete.")
        else:
            self.status_label.setText("Delete completed with failures.")
        self.stats_label.setText(
            f"Deleted {result.deleted_count} items · {format_bytes(result.total_bytes)} · {result.elapsed_sec:.2f}s"
        )
        if result.failed_count:
            QMessageBox.warning(
                self,
                "Delete Failures",
                f"Failed to delete {result.failed_count} items."
            )

    def _set_busy(self, busy: bool, status: str | None = None) -> None:
        self.choose_button.setEnabled(not busy)
        self.delete_button.setEnabled(not busy and bool(self._items))
        if status:
            self.status_label.setText(status)

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._scan_thread and self._scan_thread.isRunning():
            self._scan_thread.quit()
            self._scan_thread.wait(1000)
        self._scan_worker = None
        if self._delete_thread and self._delete_thread.isRunning():
            self._delete_thread.quit()
            self._delete_thread.wait(1000)
        self._delete_worker = None
        event.accept()
