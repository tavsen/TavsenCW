from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QGraphicsScene, QMessageBox
from PyQt5 import uic
from Facade import Facade
import sys
import logging

logging.basicConfig(level=logging.INFO)
#logging.disable(logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self, Facade):
        self.Facade = Facade
        super().__init__()
        self.ui = uic.loadUi("forms/main_menu.ui", self)
        self.window().setWindowTitle("Andrea Anderson tree. Zvarich")
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.ui.canvas.setScene(self.scene)
        self.ui.btn_add.clicked.connect(self.open_dialog_input)
        self.ui.btn_delete.clicked.connect(self.open_dialog_delete)
        self.ui.btn_save.clicked.connect(lambda: self.Facade.save_data())



    def closeEvent(self, event):
        if self.Facade.data_wait_for_save:
            logging.log(logging.INFO, ' есть несохраненные данные')
            self.save.setWindowTitle("Несохраненные данные")
            self.save.setText("Остались несохраненные данные!")
            self.save.setInformativeText("Хотите их сохранить?")

            self.save.setIcon(QMessageBox.Question)
            self.save.setStandardButtons(QMessageBox.Cancel | QMessageBox.Save)

            self.save.buttonClicked.connect(self.action)
            self.save.exec_()
        else:
            logging.log(logging.INFO, ' несохраненных данных нет')

        logging.log(logging.INFO, ' окно закрыто')

    def action(self, btn):
        if btn.text() == "Save":
            logging.log(logging.INFO, " данные сохранены")
            self.Facade.save_data()
        else:
            logging.log(logging.INFO, " данные не сохранены")

    def open_dialog_input(self):
        dialog = DialogInput(self.Facade, self)
        dialog.setWindowTitle("add val")
        dialog.show()

    def open_dialog_delete(self):
        dialog = DialogDelete(self.Facade, self)  # тут self. нужен для теста (чтобы можно было обратиться к dialog)
        dialog.setWindowTitle("Удаление данных")
        dialog.show()

    def draw_el(self, x, y, val, left=None, height=0):
        self.scene.addEllipse(x, y, 40, 40)
        long = len(str(val))
        text = self.scene.addText(f"{val}")
        text.moveBy(x + 17 - long * 3, y + 40)

        if left == 1:
            self.scene.addLine(x + 30, y - 10, x + self.branch_len + 15, y - height + 60)
        if left == 0:
            self.scene.addLine(x + 10, y - 10, x - self.branch_len + 25, y - height + 60)

    def draw_tree(self):
        self.scene.clear()
        path = self.Facade.bypass_tree()

        x = 50 * (2 ** path[0]) + 50
        y = 150
        h = 50
        height = h * path[0] + h
        self.branch_len = (x - 50) // 2
        layer = 0
        frame_x = 0
        for val in range(1, path[0] + 2):
            frame_x += h * val

        self.scene = QGraphicsScene(0, 0, x * 2 + 100, frame_x + 300)
        logging.log(logging.INFO, f' размер холста - {x * 2 + 100}, {y * path[0] + 100}')
        self.ui.canvas.setScene(self.scene)

        if len(path) != 1:
            self.draw_el(x, y, path[1][0], path[1][1])

        for n in range(2, len(path)):
            if path[n][1] is not None:
                y += height
                layer += 1

                if path[n - 1][0] > path[n][0]:
                    x -= self.branch_len
                    self.draw_el(x, y, path[n][0], path[n][1], 1, height)

                else:
                    x += self.branch_len
                    self.draw_el(x, y, path[n][0], path[n][1], 0, height)
                self.branch_len //= 2

                height -= h

            else:
                height += h
                layer -= 1
                y -= height
                self.branch_len *= 2
                if path[n - 1][0] < path[n][0]:
                    x += self.branch_len
                else:
                    x -= self.branch_len

class DialogDelete(QDialog):
    def __init__(self, Facade, parent=None):
        super(DialogDelete, self).__init__(parent)
        self.Facade = Facade
        self.ui = uic.loadUi("forms/delete.ui", self)
        self.ui.btn_remove.clicked.connect(self.delete)
        self.ui.btn_remove_all.clicked.connect(lambda: self.del_all())

    def del_all(self):
        if self.Facade.dictionary.key is not None:  # если есть данные для удаления
            self.messagebox_del_all = QMessageBox(self)
            self.messagebox_del_all.setWindowTitle("Удаление данных")
            self.messagebox_del_all.setText("Вы уверены, что хотите удалить все данные?")
            self.messagebox_del_all.setInformativeText("После сохранения данные будут утеряны!")

            self.messagebox_del_all.setIcon(QMessageBox.Question)
            self.messagebox_del_all.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)

            self.messagebox_del_all.buttonClicked.connect(self.action)
            self.messagebox_del_all.show()
        else:
            QMessageBox.warning(self, 'Удаление данных', "Данных для удаления нет", QMessageBox.Ok)

    def action(self, button):
        if button.text() == "OK":
            self.Facade.del_all_from_sbst()
            self.parent().draw_tree()
            logging.log(logging.INFO, 'Value deleted')
        else:
            logging.log(logging.INFO, 'There is no deleted data')

    def delete(self):
        link = self.Facade.search_element_in_tree(self.ui.input_key.value())  # ссылка на элемент, который удаляем
        if link is not None:
            try:
                self.ui.label_info.setText(f"Вы удалили: {self.ui.input_key.value()}, {link.data}")
                self.Facade.delete_value(self.ui.input_key.value())
                self.parent().draw_tree()
            except RecursionError:
                self.ui.label_info.setText(f"Tree is too high!")


class DialogInput(QDialog):


    def __init__(self, Facade, parent=None):
        self.Facade = Facade
        super(DialogInput, self).__init__(parent)
        self.ui = uic.loadUi("forms/input.ui", self)
        self.ui.btn_insert.clicked.connect(self.add)
    def add(self):
        if self.ui.input_value() is None:
            try:
                self.Facade.insert_value(self.ui.val_input.text())
                self.parent().draw_tree()
                logging.log(logging.INFO, 'заполните поля')
            except RecursionError:
                self.ui.label_info.setText(f"Дерево слишком высокое!")


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
