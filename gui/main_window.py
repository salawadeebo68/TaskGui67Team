import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLineEdit, QComboBox, QLabel,
    QListWidgetItem, QDialog, QDateEdit, QTextEdit,
    QCheckBox, QFrame, QScrollArea, QSizePolicy,
    QGraphicsDropShadowEffect, QApplication, QMessageBox
)
from PySide6.QtCore import Qt, QDate, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QPalette, QLinearGradient, QPainter

from services.task_manager import TaskManager
from services.notification_service import NotificationService
from gui.styles import STYLE, DIALOG_EXTRA, PRIORITY_COLORS, PRIORITY_BG


class AddTaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.setWindowTitle("เพิ่ม งาน" if not task else "แก้ไขงาน")
        self.setMinimumWidth(420)
        self.setStyleSheet(STYLE + DIALOG_EXTRA)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("" + ("เพิ่มงานใหม่" if not task else "แก้ไขงาน"))
        header.setStyleSheet("font-size:16px; font-weight:700; color:#e8e8f0; margin-bottom:4px;")
        layout.addWidget(header)

        lbl_title = QLabel("ชื่องาน")
        lbl_title.setObjectName("section_label")
        layout.addWidget(lbl_title)
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("เช่น ทำรายงาน, เขียนโค้ด...")
        layout.addWidget(self.input_title)

        row = QHBoxLayout()
        row.setSpacing(12)

        col1 = QVBoxLayout()
        lbl_dl = QLabel("กำหนดเวลา")
        lbl_dl.setObjectName("section_label")
        col1.addWidget(lbl_dl)
        self.input_deadline = QDateEdit()
        self.input_deadline.setCalendarPopup(True)
        self.input_deadline.setDate(QDate.currentDate())
        self.input_deadline.setDisplayFormat("yyyy-MM-dd")
        col1.addWidget(self.input_deadline)

        col2 = QVBoxLayout()
        lbl_pr = QLabel("PRIORITY")
        lbl_pr.setObjectName("section_label")
        col2.addWidget(lbl_pr)
        self.input_priority = QComboBox()
        self.input_priority.addItems(["High", "Medium", "Low"])
        self.input_priority.setCurrentText("Medium")
        col2.addWidget(self.input_priority)

        row.addLayout(col1)
        row.addLayout(col2)
        layout.addLayout(row)

        lbl_notes = QLabel("หมายเหตุ (ไม่บังคับ)")
        lbl_notes.setObjectName("section_label")
        layout.addWidget(lbl_notes)
        self.input_notes = QTextEdit()
        self.input_notes.setPlaceholderText("รายละเอียดเพิ่มเติม...")
        self.input_notes.setMaximumHeight(80)
        layout.addWidget(self.input_notes)

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("ยกเลิก")
        btn_cancel.setObjectName("btn_ghost")
        btn_ok = QPushButton("บันทึก")
        btn_ok.setObjectName("btn_success")
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        layout.addLayout(btn_row)

        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)

        if task:
            self.input_title.setText(task.title)
            if task.deadline:
                self.input_deadline.setDate(QDate.fromString(task.deadline, "yyyy-MM-dd"))
            self.input_priority.setCurrentText(task.priority)
            if hasattr(task, "notes"):
                self.input_notes.setPlainText(task.notes)

    def get_data(self):
        return {
            "title": self.input_title.text().strip(),
            "deadline": self.input_deadline.date().toString("yyyy-MM-dd"),
            "priority": self.input_priority.currentText(),
            "notes": self.input_notes.toPlainText().strip()
        }


class StatsBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(0)

        self.lbl_total = self._make_stat("0", "ทั้งหมด")
        self.lbl_done  = self._make_stat("0", "เสร็จแล้ว")
        self.lbl_high  = self._make_stat("0", "ยาก")
        self.lbl_over  = self._make_stat("0", "เลยกำหนด")

        for w in [self.lbl_total, self.lbl_done, self.lbl_high, self.lbl_over]:
            layout.addWidget(w)
            layout.addStretch()

    def _make_stat(self, value, label):
        frame = QFrame()
        v = QVBoxLayout(frame)
        v.setContentsMargins(8, 0, 8, 0)
        v.setSpacing(2)
        num = QLabel(value)
        num.setStyleSheet("font-size:22px; font-weight:800; color:#c4b5fd;")
        num.setAlignment(Qt.AlignCenter)
        lbl = QLabel(label)
        lbl.setStyleSheet("font-size:9px; color:#6060a0; letter-spacing:2px; font-weight:600;")
        lbl.setAlignment(Qt.AlignCenter)
        v.addWidget(num)
        v.addWidget(lbl)
        frame._num = num
        return frame

    def update_stats(self, tasks, overdue_count):
        total = len(tasks)
        done  = sum(1 for t in tasks if t.completed)
        high  = sum(1 for t in tasks if t.priority == "High" and not t.completed)
        self.lbl_total._num.setText(str(total))
        self.lbl_done._num.setText(str(done))
        self.lbl_high._num.setText(str(high))
        self.lbl_over._num.setText(str(overdue_count))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✦ Smart Task Manager")
        self.resize(780, 640)
        self.setStyleSheet(STYLE)
        self.setMinimumSize(700, 500)

        self.manager = TaskManager()
        self.notif   = NotificationService(self.manager)

        self._build_ui()
        self.refresh_tasks()

        timer = QTimer(self)
        timer.timeout.connect(self._check_notifications)
        timer.start(60000)
        QTimer.singleShot(500, self._check_notifications)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        hdr = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title = QLabel("TASK MANAGER")
        title.setObjectName("title_label")
        sub = QLabel("จัดการตารางเวลงาน")
        sub.setObjectName("subtitle_label")
        title_col.addWidget(title)
        title_col.addWidget(sub)
        hdr.addLayout(title_col)
        hdr.addStretch()
        btn_add = QPushButton("เพิ่มงานใหม่")
        btn_add.setFixedHeight(38)
        btn_add.clicked.connect(self.open_add_dialog)
        hdr.addWidget(btn_add)
        root.addLayout(hdr)

        self.stats_bar = StatsBar()
        root.addWidget(self.stats_bar)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ค้นหางาน")
        self.search_input.textChanged.connect(self.refresh_tasks)

        self.filter_priority = QComboBox()
        self.filter_priority.addItems(["All", "High", "Medium", "Low"])
        self.filter_priority.setFixedWidth(110)
        self.filter_priority.currentTextChanged.connect(self.refresh_tasks)

        self.filter_completed = QCheckBox("แสดงที่เสร็จแล้ว")
        self.filter_completed.setChecked(True)
        self.filter_completed.stateChanged.connect(self.refresh_tasks)

        filter_row.addWidget(self.search_input)
        filter_row.addWidget(self.filter_priority)
        filter_row.addWidget(self.filter_completed)
        root.addLayout(filter_row)

        self.task_list = QListWidget()
        self.task_list.setAlternatingRowColors(False)
        self.task_list.setSpacing(2)
        root.addWidget(self.task_list)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        btn_complete = QPushButton("เสร็จแล้ว")
        btn_complete.setObjectName("btn_success")
        btn_edit     = QPushButton("แก้ไข")
        btn_edit.setObjectName("btn_ghost")
        btn_delete   = QPushButton("ลบ")
        btn_delete.setObjectName("btn_danger")

        btn_complete.clicked.connect(self.complete_task)
        btn_edit.clicked.connect(self.edit_task)
        btn_delete.clicked.connect(self.delete_task)

        for b in [btn_complete, btn_edit, btn_delete]:
            b.setFixedHeight(38)
            btn_row.addWidget(b)
        root.addLayout(btn_row)

    def _make_task_item(self, task):
        color  = PRIORITY_COLORS.get(task.priority, "#a0a0c0")
        bg     = PRIORITY_BG.get(task.priority, "rgba(100,100,160,0.1)")
        done_style = "opacity:0.45; text-decoration:line-through;" if task.completed else ""
        status_icon = "✓" if task.completed else ("🔴" if task.priority == "High" else ("🟡" if task.priority == "Medium" else "🟢"))
        deadline_html = f'<span style="color:#6060a0; font-size:11px;"> · 📅 {task.deadline}</span>' if task.deadline else ""

        html = f"""
        <div style="padding:4px 0; {done_style}">
          <span style="
            background:{bg};
            color:{color};
            font-size:10px;
            font-weight:700;
            letter-spacing:1.5px;
            border-radius:4px;
            padding:2px 7px;
            margin-right:8px;
          ">{task.priority.upper()}</span>
          <span style="font-size:13px; font-weight:600; color:{'#888' if task.completed else '#e8e8f0'};">{task.title}</span>
          {deadline_html}
        </div>
        """
        return html

    def refresh_tasks(self):
        search   = self.search_input.text() if hasattr(self, "search_input") else ""
        priority = self.filter_priority.currentText() if hasattr(self, "filter_priority") else "All"
        show_done = self.filter_completed.isChecked() if hasattr(self, "filter_completed") else True

        self.current_tasks = self.manager.get_tasks(priority, search, show_done)
        self.task_list.clear()

        for task in self.current_tasks:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 52))
            self.task_list.addItem(item)

            widget = QLabel(self._make_task_item(task))
            widget.setTextFormat(Qt.RichText)
            widget.setContentsMargins(4, 0, 4, 0)
            self.task_list.setItemWidget(item, widget)

        overdue = len(self.manager.get_overdue_tasks())
        self.stats_bar.update_stats(self.manager.tasks, overdue)

    def open_add_dialog(self):
        dlg = AddTaskDialog(self)
        if dlg.exec():
            d = dlg.get_data()
            if d["title"]:
                self.manager.add_task(d["title"], d["deadline"], d["priority"], d["notes"])
                self.refresh_tasks()

    def edit_task(self):
        idx = self.task_list.currentRow()
        if idx < 0 or idx >= len(self.current_tasks):
            return
        task = self.current_tasks[idx]
        real_idx = self.manager.tasks.index(task)
        dlg = AddTaskDialog(self, task)
        dlg.setWindowTitle("แก้ไขงาน")
        if dlg.exec():
            d = dlg.get_data()
            if d["title"]:
                self.manager.edit_task(real_idx, d["title"], d["deadline"], d["priority"])
                self.refresh_tasks()

    def complete_task(self):
        idx = self.task_list.currentRow()
        if idx < 0 or idx >= len(self.current_tasks):
            return
        task = self.current_tasks[idx]
        real_idx = self.manager.tasks.index(task)
        self.manager.complete_task(real_idx)
        self.refresh_tasks()

    def delete_task(self):
        idx = self.task_list.currentRow()
        if idx < 0 or idx >= len(self.current_tasks):
            return
        task = self.current_tasks[idx]
        real_idx = self.manager.tasks.index(task)
        self.manager.delete_task(real_idx)
        self.refresh_tasks()

    def _check_notifications(self):
        alerts = self.notif.check_notifications()
        if alerts:
            msg = QMessageBox(self)
            msg.setWindowTitle("แจ้งเตือนครบกำหนด!!")
            msg.setText("\n".join(alerts))
            msg.setStyleSheet(STYLE)
            msg.exec()