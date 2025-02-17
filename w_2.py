import sqlite3

from PyQt6.QtWidgets import *
from ui_file2 import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.update_result)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.save_results2)
        self.con = sqlite3.connect("data/coffee")
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'" for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def save_results2(self):
        cur = self.con.cursor()
        que = (
            f"INSERT INTO coffee(name, degree, which, description, price, size) VALUES('{self.textEdit.toPlainText()}', "
            f"'{self.textEdit_2.toPlainText()}', '{self.textEdit_3.toPlainText()}', '{self.textEdit_4.toPlainText()}', "
            f"{self.spinBox_2.text()}, '{self.spinBox_3.text()} кг')")
        print(que)
        cur.execute(que)
        self.con.commit()
