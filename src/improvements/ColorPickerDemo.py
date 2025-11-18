import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog


class ColorDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор цвета с разными форматами")
        self.setGeometry(100, 100, 400, 300)

        self.button = QPushButton("Выбрать цвет", self)
        self.button.clicked.connect(self.choose_color)
        self.button.move(140, 130)

    def choose_color(self):
        color = QColorDialog.getColor()  # открываем стандартный диалог
        if color.isValid():
            # Печатаем разные форматы
            print("HEX:", color.name())  # #RRGGBB
            print("RGB:", color.red(), color.green(), color.blue())
            print("HSL:", color.hue(), color.saturation(), color.lightness())
            r = color.red()
            g = color.green()
            b = color.blue()

            # Собираем в одно целое число
            color_int = (r << 16) | (g << 8) | b
            print("Цвет как int:", color_int)
            # Меняем фон окна на выбранный цвет
            self.setStyleSheet(f"background-color: {color.name()};")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorDemo()
    window.show()
    sys.exit(app.exec_())
