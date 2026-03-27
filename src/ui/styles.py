"""Application styles (mac-inspired)."""

STYLE_SHEET = """
QMainWindow {
    background-color: #F7F7F8;
}
QWidget#Card {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}
QLabel#Title {
    color: #1F2328;
    font-size: 16px;
    font-weight: 600;
}
QPushButton {
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
}
QPushButton#Primary {
    background-color: #3B82F6;
    color: white;
    border: none;
}
QPushButton#Primary:hover {
    background-color: #2563EB;
}
QPushButton#Danger {
    background-color: #EF4444;
    color: white;
    border: none;
}
QPushButton#Danger:hover {
    background-color: #DC2626;
}
QPushButton#Ghost {
    background-color: transparent;
    border: 1px solid #E5E7EB;
    color: #1F2328;
}
QHeaderView::section {
    background-color: #F3F4F6;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #E5E7EB;
    font-size: 12px;
    color: #374151;
}
QTableView {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    gridline-color: #E5E7EB;
    selection-background-color: #DBEAFE;
    selection-color: #111827;
}
QTableView::item {
    padding: 4px 8px;
}
QLabel#Muted {
    color: #6B7280;
}
QLabel#Stats {
    color: #1F2328;
    font-weight: 500;
}
"""
