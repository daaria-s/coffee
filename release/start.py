import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from main import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class AddWidget(QWidget, Ui_Form):
    def __init__(self, name=''):
        super().__init__()
        s = "UI\\"
        uic.loadUi(f'UI\\addEditCoffeeForm.ui', self)  # Загружаем дизайн
        self.fill_data()
        self.red = False
        if name:
            self.red = name
            self.add_info(name)
        self.saved.clicked.connect(self.save_data)

    def add_info(self, name):
        con = sqlite3.connect('data\coffee.db')
        cur = con.cursor()
        info = cur.execute(f"""SELECT name, description, price, size
                FROM Coffee
                WHERE name = '{name}'""").fetchone()
        for n, i in enumerate([self.name, self.description, self.price, self.size]):
            i.setText(str(info[n]))
        con.close()

    def fill_data(self):
        con = sqlite3.connect('data\coffee.db')
        cur = con.cursor()
        info = cur.execute("""SELECT name FROM Sorts""").fetchall()
        for i in info:
            self.sort.addItem(i[0])
        info = cur.execute("""SELECT name FROM Types""").fetchall()
        for i in info:
            self.type.addItem(i[0])
        info = cur.execute("""SELECT name FROM Roasters""").fetchall()
        for i in info:
            self.roaster.addItem(i[0])
        con.close()

    def save_data(self):
        if self.name.text() and self.description.text() and self.price.text().isdigit() and self.size.text().isdigit():
            con = sqlite3.connect('data\coffee.db')
            cur = con.cursor()
            roaster = cur.execute(f"""SELECT id FROM Roasters WHERE name = '{self.roaster.currentText()}'""").fetchone()[0]
            type = cur.execute(f"""SELECT id FROM Types WHERE name = '{self.type.currentText()}'""").fetchone()[0]
            sort = cur.execute(f"""SELECT id FROM Sorts WHERE name = '{self.sort.currentText()}'""").fetchone()[0]
            if self.red:
                cur.execute(f"""UPDATE Coffee
                    SET name = '{self.name.text()}',
                    roaster = '{roaster}',
                    type = '{type}',
                    description = '{self.description.text()}',
                    price = {self.price.text()},
                    size = {self.size.text()},
                    sort = '{sort}'
                    WHERE name = '{self.red}'""")
            else:
                cur.execute(
                    f"""INSERT INTO Coffee(name, roaster, type, description, price, size, sort) 
                                    VALUES('{self.name.text()}', '{roaster}', '{type}', '{self.description.text()}', {self.price.text()}, {self.size.text()}, '{sort}')""").fetchall()
            con.commit()
            con.close()
            self.close()
        else:
            self.info.setText('Некорректные данные')


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI\main.ui', self)  # Загружаем дизайн
        self.show_table()
        self.add.clicked.connect(self.add_coffee)
        self.redaction.clicked.connect(self.redact)
        self.window = None

    def show_table(self):
        con = sqlite3.connect('data\coffee.db')
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
        con.close()
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

    def add_coffee(self):
        self.window = AddWidget()
        self.window.show()
        self.window.saved.clicked.connect(self.show_table)

    def redact(self):
        if self.tableWidget.currentItem():
            a = self.tableWidget.item(self.tableWidget.currentItem().row(), 0).text()
            self.window = AddWidget(a)
            self.window.show()
            self.window.saved.clicked.connect(self.show_table)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
