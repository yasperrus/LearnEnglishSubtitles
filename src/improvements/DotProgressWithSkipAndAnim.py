import math
import sys

from PyQt5.QtCore import Qt, QSize, QRect, QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout


class EasingPulsatingDotProgressBar(QWidget):
    def __init__(self, total=30, min_size=5, max_size=15, parent=None):
        super().__init__(parent)
        self.total = total
        self.min_size = min_size
        self.max_size = max_size
        self.states = ["empty"] * total
        self.current_index = 0
        self.dot_size = min_size
        self.spacing = 5
        self.rows = 1

        # Анимация
        self.highlight_progress = 1.0
        self.pulse_progress = 0.0
        self.animation_timer = QTimer()
        self.animation_timer.setInterval(16)  # ~60 FPS
        self.animation_timer.timeout.connect(self.update_animation)

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
            if self.states[self.current_index] == "empty":
                self.states[self.current_index] = "skipped"
            self.current_index += 1
            self.start_animation()
            self.update()

    def move_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.start_animation()
            self.update()

    def start_animation(self):
        self.highlight_progress = 0.0
        self.pulse_progress = 0.0
        self.animation_timer.start()

    def update_animation(self):
        self.highlight_progress = min(1.0, self.highlight_progress + 0.08)
        # easing пульсации: sin(pi * t)
        self.pulse_progress += 0.08
        if self.pulse_progress >= math.pi:
            self.pulse_progress = math.pi
            self.animation_timer.stop()
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
            base_size = self.dot_size
            x = col * (self.dot_size + self.spacing)
            y = row * (self.dot_size + self.spacing)

            if i == self.current_index:
                # easing пульсации с sin(pi * t)
                scale = 1.0 + 0.3 * math.sin(self.pulse_progress)
                size = int(base_size * scale)
                offset = (base_size - size) // 2
                rect = QRect(x + offset, y + offset, size, size)

                # плавное смешение цвета с белым
                base_color = (
                    QColor("#B0BEC5")
                    if state == "empty"
                    else (
                        QColor("#4CAF50")
                        if state == "correct"
                        else (
                            QColor("#F44336") if state == "wrong" else QColor("#2196F3")
                        )
                    )
                )
                r = (
                    base_color.red()
                    + (255 - base_color.red()) * self.highlight_progress
                )
                g = (
                    base_color.green()
                    + (255 - base_color.green()) * self.highlight_progress
                )
                b = (
                    base_color.blue()
                    + (255 - base_color.blue()) * self.highlight_progress
                )
                color = QColor(int(r), int(g), int(b))
            else:
                size = base_size
                rect = QRect(x, y, size, size)
                if state == "correct":
                    color = QColor("#4CAF50")
                elif state == "wrong":
                    color = QColor("#F44336")
                elif state == "skipped":
                    color = QColor("#2196F3")
                else:
                    color = QColor("#B0BEC5")

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

    progress = EasingPulsatingDotProgressBar(total=30, min_size=1, max_size=5)
    layout.addWidget(progress)

    nav_layout = QHBoxLayout()
    btn_prev = QPushButton("Назад")
    btn_next = QPushButton("Вперед")
    nav_layout.addWidget(btn_prev)
    nav_layout.addWidget(btn_next)
    layout.addLayout(nav_layout)

    btn_correct = QPushButton("Правильный")
    btn_wrong = QPushButton("Неправильный")
    layout.addWidget(btn_correct)
    layout.addWidget(btn_wrong)

    btn_correct.clicked.connect(
        lambda: [
            progress.set_dot(progress.current_index, "correct"),
            progress.move_next(),
        ]
    )
    btn_wrong.clicked.connect(
        lambda: [
            progress.set_dot(progress.current_index, "wrong"),
            progress.move_next(),
        ]
    )
    btn_prev.clicked.connect(progress.move_prev)
    btn_next.clicked.connect(progress.move_next)

    win.resize(800, 300)
    win.show()
    sys.exit(app.exec_())
