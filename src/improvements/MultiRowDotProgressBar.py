import math
import sys

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class AdaptiveDotProgressBar(QWidget):
    def __init__(self, total=100, min_size=10, max_size=30, parent=None):
        super().__init__(parent)
        self.total = total
        self.min_size = min_size
        self.max_size = max_size
        self.states = ["empty"] * total
        self.dot_size = min_size
        self.spacing = 5
        self.rows = 1
        self.setMinimumHeight(self.dot_size + self.spacing)

    def set_dot(self, index, state):
        if 0 <= index < self.total and state in ("empty", "correct", "wrong"):
            self.states[index] = state
            self.update()

    def resizeEvent(self, event):
        width = self.width()
        # сначала пробуем поместить все в один ряд
        max_dot_space = width / self.total
        dot_size = min(self.max_size, int(max_dot_space * 0.7))
        spacing = int(max_dot_space * 0.3)

        # если dot_size < min_size, нужно увеличить количество рядов
        if dot_size < self.min_size:
            per_row = max(1, width // (self.min_size + spacing))
            self.rows = math.ceil(self.total / per_row)
            per_row = math.ceil(self.total / self.rows)
            dot_size = min(
                self.max_size, max(self.min_size, int((width / per_row) * 0.7))
            )
            spacing = int((width / per_row) * 0.3)
        else:
            self.rows = 1

        self.dot_size = dot_size
        self.spacing = spacing
        self.setFixedHeight(self.rows * (self.dot_size + self.spacing))
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        per_row = math.ceil(self.total / self.rows)
        for i, state in enumerate(self.states):
            row = i // per_row
            col = i % per_row
            x = col * (self.dot_size + self.spacing)
            y = row * (self.dot_size + self.spacing)
            rect = QRect(x, y, self.dot_size, self.dot_size)
            if state == "correct":
                color = QColor("#4CAF50")
            elif state == "wrong":
                color = QColor("#F44336")
            else:
                color = QColor("#B0BEC5")
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(rect)

    def sizeHint(self):
        return QSize(self.total, self.rows * (self.dot_size + self.spacing))


# --- тест ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    layout = QVBoxLayout(win)

    progress = AdaptiveDotProgressBar(total=300, min_size=4, max_size=8)
    layout.addWidget(progress)

    btn_correct = QPushButton("Правильный ответ")
    btn_wrong = QPushButton("Неправильный ответ")
    layout.addWidget(btn_correct)
    layout.addWidget(btn_wrong)

    current_index = [0]

    def add_correct():
        if current_index[0] < progress.total:
            progress.set_dot(current_index[0], "correct")
            current_index[0] += 1

    def add_wrong():
        if current_index[0] < progress.total:
            progress.set_dot(current_index[0], "wrong")
            current_index[0] += 1

    btn_correct.clicked.connect(add_correct)
    btn_wrong.clicked.connect(add_wrong)

    win.resize(800, 300)
    win.show()
    sys.exit(app.exec_())
