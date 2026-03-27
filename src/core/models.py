"""Core data structures for scan and delete operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Item:
    path: str
    is_dir: bool
    size_bytes: int
    mtime: float


@dataclass
class DeleteResult:
    deleted_count: int
    failed_count: int
    failed_items: List[Item]
    total_bytes: int
    elapsed_sec: float
