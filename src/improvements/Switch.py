from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget


# ------------------ Компактный Switch на QWidget ------------------
class Switch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, text="", checked=False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self._text = text
        self._bg_color = QColor("#4CAF50") if checked else QColor("#B0BEC5")
        self.setMinimumHeight(22)  # можно подогнать под UI
        self.setContentsMargins(0, 0, 0, 0)

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self._bg_color = QColor("#4CAF50") if self._checked else QColor("#B0BEC5")
        self.update()
        self.toggled.emit(self._checked)

    def isChecked(self):
        return self._checked

    def setChecked(self, state: bool):
        self._checked = state
        self._bg_color = QColor("#4CAF50") if state else QColor("#B0BEC5")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        padding = 1
        circle_d = min(h - 2 * padding, 18)
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

        # текст
        if self._text:
            text_rect = QRect(bg_w + 2 * padding, 0, w - bg_w - 3 * padding, h)
            painter.setPen(QColor("#333"))
            painter.setFont(QFont("Arial", 10))
            metrics = QFontMetrics(self.font())
            elided_text = metrics.elidedText(
                self._text, Qt.ElideRight, text_rect.width()
            )
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, elided_text)


# ------------------ Функции замены чекбоксов ------------------
def replace_checkbox_with_switch(checkbox: QtWidgets.QCheckBox) -> Switch:
    parent = checkbox.parent()
    layout = parent.layout() if parent else None

    switch = Switch(parent=parent, checked=checkbox.isChecked(), text=checkbox.text())

    # подключаем toggle
    try:
        checkbox.toggled.disconnect()
    except Exception:
        pass
    checkbox.toggled.connect(switch.setChecked)

    # используем размер исходного QCheckBox как минимум
    sh = checkbox.sizeHint()
    switch.setMinimumSize(sh)
    switch.setMaximumHeight(sh.height())

    # вставляем на то же место
    if layout:
        index = layout.indexOf(checkbox)
        layout.removeWidget(checkbox)
        checkbox.setParent(None)
        layout.insertWidget(index, switch)

    return switch


def replace_all_checkboxes(widget):
    for cb in widget.findChildren(QtWidgets.QCheckBox):
        replace_checkbox_with_switch(cb)
