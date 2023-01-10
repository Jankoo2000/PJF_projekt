import sys
from datetime import datetime

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from gui_loty import Ui_MainWindow
from _backend import  azair


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1470, 450)
        self.loadProducts()
        self.ui.add_button.clicked.connect(self.data_save)
        self.ui.remove_button.clicked.connect(self.remove_row)
        self.ui.close_button.clicked.connect(self.close)
        self.ui.execute_button.clicked.connect(self.execute)
        self.ui.info_button.clicked.connect(self.info)
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def info(self):
        question = QMessageBox.question(self, "INFO",
                                        "DATE FORMAT: YYYY-MM-DD \n" +
                                        "MIN_DAYS, MAX_DAYS: <0, RETURN - DEPART> \n" +
                                        "MIN_DAYS <= MAX_DAYS\n" +
                                        "MIN_DAYS,MAX_DAYS, PRICE is decimal",

                                        QMessageBox.Ok)
    def clear_line(self):
        from_line = self.ui.line_from.clear()
        to_line = self.ui.line_to.clear()
        depart_line = self.ui.line_depart_date.clear()
        return_line = self.ui.line_return_date.clear()
        max_line = self.ui.line_max_days.clear()
        min_line = self.ui.line_min_days.clear()
        price_line = self.ui.line_price.clear()

    def data_save(self):

        from_line = self.ui.line_from.text()
        to_line = self.ui.line_to.text()
        depart_line = self.ui.line_depart_date.text()
        return_line = self.ui.line_return_date.text()
        max_line = self.ui.line_max_days.text()
        min_line = self.ui.line_min_days.text()
        price_line = self.ui.line_price.text()

        days_between_dep_arr =  lambda x, y: abs(datetime.strptime(x, "%Y-%m-%d") - datetime.strptime(y, "%Y-%m-%d")).days
        try :
            if(
                    from_line is not None
                    and to_line is not None
                    and depart_line is not None and bool(datetime.strptime(depart_line, "%Y-%m-%d")) and len(depart_line.split('-')[1]) == 2
                    and return_line is not None and bool(datetime.strptime(return_line, "%Y-%m-%d")) and len(return_line.split('-')[1]) == 2
                    and min_line is not None and isinstance(int(min_line), int) and int(min_line) >= 0 and int(min_line) <= days_between_dep_arr(depart_line,return_line)
                    and max_line is not None and isinstance(int(max_line), int) and int(max_line) >= 0 and int(max_line) <= days_between_dep_arr(depart_line,return_line) and int(max_line) >= int(min_line)
                    and price_line is not None and isinstance(int(price_line), int)
                    and from_line and to_line and depart_line and return_line and max_line and min_line and  price_line is not None):

                rowCount = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowCount)
                self.ui.tableWidget.setItem(rowCount,0,QTableWidgetItem(from_line))
                self.ui.tableWidget.setItem(rowCount,1,QTableWidgetItem(to_line))
                self.ui.tableWidget.setItem(rowCount,2,QTableWidgetItem(depart_line))
                self.ui.tableWidget.setItem(rowCount,3,QTableWidgetItem(return_line))
                self.ui.tableWidget.setItem(rowCount,4,QTableWidgetItem(min_line))
                self.ui.tableWidget.setItem(rowCount,5,QTableWidgetItem(max_line))
                self.ui.tableWidget.setItem(rowCount,6,QTableWidgetItem(price_line))
                self.data_save_to_file()
            else:
                question = QMessageBox.question(self, "Remove Flight",
                                                "Wprowadz poprawne dane 1",
                                                QMessageBox.Ok)

        except:
            question = QMessageBox.question(self, "Remove Flight",
                                            "Wprowadz poprawne dane 2",
                                            QMessageBox.Ok)


        # self.clear_line()


    def data_save_to_file(self):
        table = self.ui.tableWidget
        col_count = table.columnCount()
        row_count = table.rowCount()
        headers = [str(table.horizontalHeaderItem(i).text()) for i in range(col_count)]

        df_list = []

        for row in range(row_count):
            df_list2 = []
            for col in range(col_count):
                table_item = table.item(row, col)
                df_list2.append('' if table_item is None else str(table_item.text()))
            df_list.append(df_list2)

        df = pd.DataFrame(df_list, columns=headers)
        print(df)
        df.to_csv('1.csv')

    def remove_row(self):
        currentRow = self.ui.tableWidget.currentRow()

        question = QMessageBox.question(self,"Remove Flight",
                                        "Do you want to remove flight?",
                                        QMessageBox.Yes | QMessageBox.No)
        #
        if question == QMessageBox.Yes:
            self.ui.tableWidget.removeRow(currentRow)

        self.data_save_to_file()



    def loadProducts(self):

        df = None
        try:
            df = pd.read_csv('1.csv')
        except:
            pd.DataFrame(columns=['FROM', 'TO', 'DEPART DATE', 'RETURN DATE', 'MIN DAYS',
                                  'MAX DAYS', 'PRICE']).to_csv("1.csv")
            df = pd.read_csv('1.csv')


        self.ui.tableWidget.setRowCount(len(df.index)) # ile wieszy
        self.ui.tableWidget.setColumnCount(7) ## ile kolumn

        self.ui.tableWidget.setHorizontalHeaderLabels(('FROM','TO', 'DEPART DATE', 'RETURN DATE', 'MIN DAYS', 'MAX DAYS', 'PRICE'))


        row_index = 0
        for product in df.index:
            self.ui.tableWidget.setItem(row_index,0,QTableWidgetItem(str(df['FROM'][product])))
            self.ui.tableWidget.setItem(row_index,1,QTableWidgetItem(str(df['TO'][product])))
            self.ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(str(df['DEPART DATE'][product])))
            self.ui.tableWidget.setItem(row_index, 3, QTableWidgetItem(str(df['RETURN DATE'][product])))
            self.ui.tableWidget.setItem(row_index, 4, QTableWidgetItem(str(df['MIN DAYS'][product])))
            self.ui.tableWidget.setItem(row_index, 5, QTableWidgetItem(str(df['MAX DAYS'][product])))
            self.ui.tableWidget.setItem(row_index, 6, QTableWidgetItem(str(df['PRICE'][product])))
            row_index += 1

    def execute(self):
            azair.start()




def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

create_app()