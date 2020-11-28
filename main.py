import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.show_table()

    def show_table(self):
        con = sqlite3.connect('coffee.db')
        cur = con.cursor()
        info = cur.execute("""SELECT Coffee.name, Sorts.name, Types.name, Roasters.name, description, price, size
        FROM Coffee 
        LEFT OUTER JOIN Roasters
        ON Roasters.id = Coffee.roaster
        LEFT OUTER JOIN Types 
        ON Types.id = Coffee.type
        LEFT OUTER JOIN Sorts
        ON Sorts.id = Coffee.sort
        """).fetchall()
        print(info)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Название', 'Сорт', 'Тип', 'Обжарка', 'Описание вкуса', 'Цена(руб)',
             'Объем упаковки(г)'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(info):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
