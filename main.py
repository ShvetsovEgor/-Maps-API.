import os
import sys
from PyQt5 import uic
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.pushButton.clicked.connect(self.getImage)
        self.delta = "0.002"

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Down:
    #         self.delta = str(float(self.delta) - 0.01)
    #     if event.key() == Qt.Key_Up:
    #         self.delta = str(float(self.delta) + 0.01)
    #     print("Масштабирую")

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = str(self.doubleSpinBox.value())
        lat = str(self.doubleSpinBox_2.value())
        print(lon, lat)


        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.reload_map()

    def reload_map(self):
        # self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)

        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
