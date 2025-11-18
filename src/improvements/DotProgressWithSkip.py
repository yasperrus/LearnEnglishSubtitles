import math
import sys

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout


class NavigationDotProgressBar(QWidget):
    def __init__(self, total=20, min_size=15, max_size=30, parent=None):
        super().__init__(parent)
        self.total = total
        self.min_size = min_size
        self.max_size = max_size
        self.states = ["empty"] * total
        self.current_index = 0
        self.dot_size = min_size
        self.spacing = 5
        self.rows = 1
        self.setMinimumHeight(self.dot_size + self.spacing)

    def set_dot(self, index, state):
        if 0 <= index < self.total and state in (
            "empty",
            "correct",
            "wrong",
            "skipped",
        ):
            self.states[index] = state
            self.update()

    def move_next(self):
        if self.current_index < self.total - 1:
            # если кружок ещё не имеет оценки, отмечаем как skipped
            if self.states[self.current_index] == "empty":
                self.states[self.current_index] = "skipped"
            self.current_index += 1
            self.update()

    def move_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update()

    def resizeEvent(self, event):
        width = self.width()
        max_dot_space = width / self.total
        dot_size = min(self.max_size, int(max_dot_space * 0.7))
        spacing = int(max_dot_space * 0.3)
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

            if i == self.current_index:
                color = QColor("#FFFFFF")  # текущий кружок белый
            elif state == "correct":
                color = QColor("#4CAF50")
            elif state == "wrong":
                color = QColor("#F44336")
            elif state == "skipped":
                color = QColor("#2196F3")  # синий
            else:
                color = QColor("#B0BEC5")  # empty серый

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(rect)

    def sizeHint(self):
        return QSize(self.total, self.rows * (self.dot_size + self.spacing))


# --- тестовое окно ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    layout = QVBoxLayout(win)

    progress = NavigationDotProgressBar(total=30, min_size=15, max_size=30)
    layout.addWidget(progress)

    btn_layout = QHBoxLayout()
    btn_prev = QPushButton("Назад")
    btn_next = QPushButton("Вперед")
    btn_layout.addWidget(btn_prev)
    btn_layout.addWidget(btn_next)
    layout.addLayout(btn_layout)

    btn_correct = QPushButton("Правильный")
    btn_wrong = QPushButton("Неправильный")
    layout.addWidget(btn_correct)
    layout.addWidget(btn_wrong)

    def mark_correct():
        progress.set_dot(progress.current_index, "correct")
        progress.move_next()

    def mark_wrong():
        progress.set_dot(progress.current_index, "wrong")
        progress.move_next()

    btn_correct.clicked.connect(mark_correct)
    btn_wrong.clicked.connect(mark_wrong)
    btn_prev.clicked.connect(progress.move_prev)
    btn_next.clicked.connect(progress.move_next)

    win.resize(800, 250)
    win.show()
    sys.exit(app.exec_())
