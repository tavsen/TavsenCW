from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QListWidgetItem, QMessageBox
from PyQt5 import uic
from Facade import Facade
import sys
import logging

logging.basicConfig(level=logging.INFO)



class MainWindow(QMainWindow):
    def __init__(self, Facade):
        self.Facade = Facade
        super().__init__()
        self.ui = uic.loadUi("forms/main_menu.ui", self)
        self.window().setWindowTitle("Andrea Anderson tree. Zvarich")
        self.ui.btn_add.clicked.connect(self.open_dialog_input)
        self.ui.btn_delete.clicked.connect(self.open_dialog_delete)
        self.ui.btn_save.clicked.connect(lambda: self.Facade.save_data())
    def closeEvent(self, event):
        if self.Facade.data_wait_for_save:
            logging.log(logging.INFO, ' You have unsaved Data')
            self.save.setWindowTitle("Warning")
            self.save.setText("You have got unsaved data!")
            self.save.setInformativeText("Would you like to save it?")
            self.save.setIcon(QMessageBox.Question)
            self.save.setStandardButtons(QMessageBox.Cancel | QMessageBox.Save)
            self.save.buttonClicked.connect(self.action)
            self.save.exec_()
        else:
            logging.log(logging.INFO, ' There is no unsaved data')

        logging.log(logging.INFO, ' Window closed')

    def action(self, btn):
        if btn.text() == "Save":
            logging.log(logging.INFO, " Data saved ")
            self.Facade.save_data()
        else:
            logging.log(logging.INFO, " Data unsaved ")

    def open_dialog_input(self):
        dialog = DialogInput(self.Facade, self)
        dialog.setWindowTitle("Add Data")
        dialog.show()

    def open_dialog_delete(self):
        dialog = DialogDelete(self.Facade, self)
        dialog.setWindowTitle("Delete Data")
        dialog.show()


class DialogDelete(QDialog):
    def __init__(self, Facade, val=None):
        super(DialogDelete, self).__init__(val)
        self.Facade = Facade
        self.ui = uic.loadUi("forms/delete.ui", self)
        self.ui.btn_remove.clicked.connect(self.delete)

    def action(self, button):
        if button.text() == "OK":
            self.Facade.del_all_from_sbst()
            self.parent().draw_tree()
            logging.log(logging.INFO, 'Data deleted')
        else:
            logging.log(logging.INFO, 'Data is not deleted')

    def delete(self):
        link = self.Facade.remove_value
        if link is not None:
            try:
                self.ui.label_info.setText(f"You deleted:{link.remove()}")
                self.Facade.remove_value()
            except RecursionError:
                self.ui.label_info.setText(f"Tree is too high")


class DialogInput(QDialog):
    def __init__(self, Facade, val=None):
        self.Facade = Facade
        super(DialogInput, self).__init__(val)
        self.ui = uic.loadUi("forms/input.ui", self)
        self.ui.btn_insert.clicked.connect(self.addact)
        self.ui.btn_insert.clicked.connect(self.showval)
    def addact(self):
         val = self.ui.data_add.text()
         self.Facade.add_value(int(val))
    def showval(self):
        self.ui.data_add.text()
        self.Facade.bypass_tree(1)
        self.list.addItems(self.bypass_tree)

class Builder:
    def __init__(self):
        self.Facade = None
        self.gui = None

    def create_Facade(self):
        self.Facade = Facade()


    def create_gui(self):
        if self.Facade is not None:
            self.gui = MainWindow(self.Facade)

    def get_result(self):
        if self.Facade is not None and self.gui is not None:
            return self.gui


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    builder = Builder()
    builder.create_Facade()
    builder.create_gui()
    window = builder.get_result()
    window.show()

    qapp.exec()
