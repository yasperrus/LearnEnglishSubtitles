import sys

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class DotProgressBar(QWidget):
    def __init__(self, total=10, parent=None):
        super().__init__(parent)
        self.total = total
        self.states = ["empty"] * total
        self.dot_size = 20
        self.spacing = 8
        self.setMinimumHeight(20)

    def set_dot(self, index, state):
        """Установить состояние кружка: 'correct', 'wrong' или 'empty'"""
        if 0 <= index < self.total and state in ("empty", "correct", "wrong"):
            self.states[index] = state
            self.update()

    def resizeEvent(self, event):
        """Пересчитать dot_size и spacing при изменении ширины"""
        width = self.width()
        if self.total > 0:
            max_total_space = width - 10  # небольшой отступ
            total_space = max_total_space / self.total
            self.dot_size = min(30, int(total_space * 0.7))  # максимум 30 px
            self.spacing = int(total_space * 0.3)
        self.setFixedHeight(self.dot_size)
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for i, state in enumerate(self.states):
            x = i * (self.dot_size + self.spacing)
            rect = QRect(x, 0, self.dot_size, self.dot_size)
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
        width = self.total * self.dot_size + (self.total - 1) * self.spacing
        return QSize(width, self.dot_size)


# --- тестовое окно ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    layout = QVBoxLayout(win)

    progress = DotProgressBar(total=20)  # большое количество кружков
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

    win.resize(600, 100)
    win.show()
    sys.exit(app.exec_())
