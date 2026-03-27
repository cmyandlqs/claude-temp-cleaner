"""Formatting helpers for UI."""

from __future__ import annotations

import datetime


def format_bytes(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def format_mtime(epoch: float) -> str:
    if epoch <= 0:
        return "-"
    dt = datetime.datetime.fromtimestamp(epoch)
    return dt.strftime("%Y-%m-%d %H:%M")
