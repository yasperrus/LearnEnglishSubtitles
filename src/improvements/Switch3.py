from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import (
    QCheckBox,
)


# ------------------ Кастомный Switch ------------------
class Switch(QCheckBox):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, checked=False, text=""):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self._checked = checked
        self._bg_color = QColor("#4CAF50") if checked else QColor("#B0BEC5")
        self._text = text
        self.setText(text)

    def sizeHint(self):
        return super().sizeHint()

    def mousePressEvent(self, event):
        self.setChecked(not self._checked)

    def setChecked(self, state: bool):
        if self._checked == state:
            return
        self._checked = state
        self._bg_color = QColor("#4CAF50") if state else QColor("#B0BEC5")
        self.update()
        self.toggled.emit(state)

    def isChecked(self):
        return self._checked

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        padding = 2
        circle_d = min(h - padding * 2, 18)
        bg_w = circle_d * 2
        bg_h = circle_d

        # фон
        painter.setBrush(QBrush(self._bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            padding, (h - bg_h) // 2, bg_w, bg_h, bg_h / 2, bg_h / 2
        )

        # кружок
        circle_x = padding if not self._checked else padding + bg_w - circle_d
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(QRect(circle_x, (h - circle_d) // 2, circle_d, circle_d))

        # текст справа
        if self._text:
            text_rect = QRect(bg_w + padding * 2, 0, w - bg_w - padding * 3, h)
            painter.setPen(QColor("#333"))
            painter.setFont(self.font())
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self._text)


# ------------------ Функция замены одного чекбокса ------------------
def replace_checkbox_with_switch(checkbox: QCheckBox) -> Switch:
    parent = checkbox.parent()
    layout = parent.layout() if parent else None

    switch = Switch(parent=parent, checked=checkbox.isChecked(), text=checkbox.text())

    # подключаем toggle
    try:
        checkbox.toggled.disconnect()
    except Exception:
        pass
    checkbox.toggled.connect(switch.setChecked)

    # заменяем в layout на том же месте
    if layout:
        index = layout.indexOf(checkbox)
        layout.removeWidget(checkbox)
        checkbox.setParent(None)
        layout.insertWidget(index, switch)

    return switch


# ------------------ Функция замены всех QCheckBox рекурсивно ------------------
def replace_all_checkboxes(widget):
    for child in widget.findChildren(QCheckBox):
        replace_checkbox_with_switch(child)
