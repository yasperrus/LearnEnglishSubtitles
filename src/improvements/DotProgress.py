import sys

from PyQt5.QtCore import Qt, QTimer, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class DotProgressBar(QWidget):
    def __init__(self, total=100, parent=None):
        super().__init__(parent)
        self.total = total
        self.current = 0
        self.displayed = 0
        self.dot_size = 20
        self.spacing = 8
        self.setMinimumHeight(20)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.animate)

    def set_progress(self, value):
        value = max(0, min(value, self.total))
        self.current = value
        if not self.timer.isActive():
            self.timer.start()

    def animate(self):
        if self.displayed < self.current:
            self.displayed += 1
            self.update()
        elif self.displayed > self.current:
            self.displayed -= 1
            self.update()
        else:
            self.timer.stop()

    def resizeEvent(self, event):
        """Пересчитать размер кружков и spacing при изменении ширины"""
        width = self.width()
        max_total_space = width - 10  # небольшой отступ слева и справа
        total_space = max_total_space / self.total
        self.dot_size = min(30, int(total_space * 0.7))  # максимум 30 px
        self.spacing = int(total_space * 0.3)
        self.setFixedHeight(self.dot_size)
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for i in range(self.total):
            x = i * (self.dot_size + self.spacing)
            rect = QRect(x, 0, self.dot_size, self.dot_size)
            color = QColor("#4CAF50") if i < self.displayed else QColor("#B0BEC5")
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
    win.setWindowTitle("Dynamic Dot ProgressBar")
    layout = QVBoxLayout(win)

    progress = DotProgressBar(total=100)
    layout.addWidget(progress)

    btn_inc = QPushButton("Добавить слово")
    layout.addWidget(btn_inc)

    words = []

    def add_word():
        words.append("word")
        progress.set_progress(len(words))

    btn_inc.clicked.connect(add_word)

    win.resize(400, 100)  # стартовый размер окна
    win.show()
    sys.exit(app.exec_())
