import os
import sys
import traceback

from PyQt5 import uic
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

# Широта Долгота
# 51,533562 46,034266 Саратов, Театральная пл-дь
# 55,753630 37,620070 Москва, Красная пл-дь
SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.pushButton.clicked.connect(self.changelonlat)
        self.map_file = False
        self.zoom = 10

    def keyPressEvent(self, event):
        get_map = False
        # if event.key() == Qt.Key_Down:
        #     self.lat -= 0.2
        #     get_map = True
        #
        # if event.key() == Qt.Key_Up:
        #     self.lat += 0.2
        #     get_map = True
        # if event.key() == Qt.Key_Right:
        #     self.lon += 0.2
        #     get_map = True
        #
        # if event.key() == Qt.Key_Left:
        #     self.lon -= 0.2
        #     get_map = True

        if event.key() == Qt.Key_PageUp:
            if self.zoom > 1:
                self.zoom -= 1
                get_map = True
        if event.key() == Qt.Key_PageDown:
            if self.zoom < 17:
                self.zoom += 1
                get_map = True
        if self.map_file and get_map:
            self.getImage()
            print(self.zoom)

    def changelonlat(self):
        self.lon = self.doubleSpinBox.value()
        self.lat = self.doubleSpinBox_2.value()

        self.getImage()

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        delta = "0.002"
        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            # "spn": ",".join([delta, delta]),
            "z": str(self.zoom),
            "l": "map"
        }
        print(api_server + "?" + "&".join([f"{x}={params[x]}" for x in params.keys()]))
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
        print("Отрисовка карты")
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

    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("Oбнаружена ошибка !:", tb)

        #    QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось

    sys.excepthook = excepthook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
