import sys

from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QPen
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
)


class Switch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, checked=False, text=""):
        super().__init__(parent)
        self._checked = checked
        self._hovered = False

        # размеры
        self.bg_width = 50
        self.bg_height = 28
        self.circle_diameter = 24
        self._circle_pos = (
            2 if not checked else self.bg_width - self.circle_diameter - 2
        )
        self._bg_color = QColor("#4CAF50") if checked else QColor("#B0BEC5")
        self._text = text
        self.setFixedSize(self.bg_width + 80, self.bg_height)  # +80 для текста справа

    # --- события ---
    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setChecked(not self._checked)

    def setChecked(self, state: bool):
        if self._checked == state:
            return
        self._checked = state
        self.animate()
        self.toggled.emit(self._checked)

    def isChecked(self):
        return self._checked

    # --- анимации ---
    def animate(self):
        # движение кружка
        anim = QPropertyAnimation(self, b"circle_pos", self)
        anim.setDuration(200)
        anim.setStartValue(self._circle_pos)
        anim.setEndValue(
            self.bg_width - self.circle_diameter - 2 if self._checked else 2
        )
        anim.start()
        self.anim = anim

        # цвет фона
        color_anim = QPropertyAnimation(self, b"bg_color", self)
        color_anim.setDuration(200)
        color_anim.setStartValue(self._bg_color)
        color_anim.setEndValue(
            QColor("#4CAF50") if self._checked else QColor("#B0BEC5")
        )
        color_anim.start()
        self.color_anim = color_anim

    # --- отрисовка ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # фон
        painter.setBrush(QBrush(self._bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(0, 0, self.bg_width, self.bg_height), 14, 14)

        # hover подсветка вокруг кружка
        if self._hovered:
            glow_color = QColor(255, 255, 255, 60)  # полупрозрачная белая
            painter.setBrush(QBrush(glow_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                QRect(
                    self._circle_pos - 2,
                    0,
                    self.circle_diameter + 4,
                    self.circle_diameter + 4,
                )
            )

        # кружок (фиксированный размер)
        circle_rect = QRect(
            self._circle_pos, 2, self.circle_diameter, self.circle_diameter
        )
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawEllipse(circle_rect)

        # иконка внутри кружка (по центру)
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        icon = "✓" if self._checked else "✕"
        painter.drawText(circle_rect, Qt.AlignCenter, icon)

        # текст справа
        if self._text:
            painter.setPen(QColor("#333"))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(self.bg_width + 5, 19, self._text)

    # --- свойства для анимации ---
    def get_circle_pos(self):
        return self._circle_pos

    def set_circle_pos(self, pos):
        self._circle_pos = pos
        self.update()

    circle_pos = pyqtProperty(int, get_circle_pos, set_circle_pos)

    def get_bg_color(self):
        return self._bg_color

    def set_bg_color(self, color):
        self._bg_color = color
        self._bg_color = color
        self.update()

    bg_color = pyqtProperty(QColor, get_bg_color, set_bg_color)


# --- тестовое окно с темой Switch ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    win.setWindowTitle("Switch Theme Demo")
    layout = QVBoxLayout(win)

    # рамка темы
    group = QGroupBox("Switch Theme")
    group_layout = QVBoxLayout(group)

    # несколько переключателей
    switches = [
        Switch(text="Power"),
        Switch(text="Wi-Fi", checked=True),
        Switch(text="Bluetooth"),
    ]

    labels = [QLabel("OFF"), QLabel("ON"), QLabel("OFF")]

    for s, l in zip(switches, labels):

        def make_toggled(lbl):
            return lambda state: lbl.setText("ON" if state else "OFF")

        s.toggled.connect(make_toggled(l))
        row = QHBoxLayout()
        row.addWidget(s)
        row.addWidget(l)
        group_layout.addLayout(row)

    layout.addWidget(group)
    win.show()
    sys.exit(app.exec_())
