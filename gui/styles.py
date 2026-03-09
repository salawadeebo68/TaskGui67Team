PRIORITY_COLORS = {
    "High":   "#ef4444",
    "Medium": "#f59e0b",
    "Low":    "#10b981",
}

PRIORITY_BG = {
    "High":   "rgba(239,68,68,0.15)",
    "Medium": "rgba(245,158,11,0.15)",
    "Low":    "rgba(16,185,129,0.15)",
}

STYLE = """
QWidget {
    background-color: #0f0f1a;
    color: #e8e8f0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

QLineEdit, QComboBox, QDateEdit, QTextEdit {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e8e8f0;
    font-size: 13px;
    selection-background-color: #7c3aed;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
    border: 1.5px solid #7c3aed;
    background: #1e1e35;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    selection-background-color: #7c3aed;
    border-radius: 8px;
    padding: 4px;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c3aed, stop:1 #5b21b6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8b5cf6, stop:1 #6d28d9);
}
QPushButton:pressed {
    background: #5b21b6;
}

QPushButton#btn_danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #991b1b);
}
QPushButton#btn_danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ef4444, stop:1 #b91c1c);
}

QPushButton#btn_success {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #059669, stop:1 #047857);
}
QPushButton#btn_success:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #10b981, stop:1 #059669);
}

QPushButton#btn_ghost {
    background: transparent;
    border: 1px solid #2a2a4a;
    color: #a0a0c0;
}
QPushButton#btn_ghost:hover {
    background: #1a1a2e;
    border-color: #7c3aed;
    color: #e8e8f0;
}

QListWidget {
    background: transparent;
    border: none;
    outline: none;
    spacing: 4px;
}
QListWidget::item {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 3px 0px;
    color: #e8e8f0;
}
QListWidget::item:selected {
    background: #1e1a3e;
    border: 1px solid #7c3aed;
    color: #ffffff;
}
QListWidget::item:hover {
    background: #1e1e35;
    border-color: #4a4a6a;
}

QScrollBar:vertical {
    background: #0f0f1a;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #2a2a4a;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #7c3aed;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QLabel#title_label {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 1px;
}
QLabel#subtitle_label {
    font-size: 12px;
    color: #6060a0;
    letter-spacing: 2px;
}
QLabel#section_label {
    font-size: 11px;
    color: #6060a0;
    font-weight: 600;
    letter-spacing: 1.5px;
    padding: 4px 0px;
}

QFrame#card {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 16px;
}

QCheckBox {
    color: #a0a0c0;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #4a4a6a;
    background: #0f0f1a;
}
QCheckBox::indicator:checked {
    background: #7c3aed;
    border-color: #7c3aed;
}
"""

DIALOG_EXTRA = """
QDialog {
    background: #13132a;
    border: 1px solid #2a2a4a;
    border-radius: 16px;
}
"""