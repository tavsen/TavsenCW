import logging
import sys

from PyQt5.QtCore import QObject, pyqtSignal

from DB_AA import DataBase
from AA import sbst


class Facade(QObject):
    """
    Класс фасада (шаблона проектирования)
    """
    update_datas = pyqtSignal()
    def __init__(self, name='Tree_data.db'):
        super().__init__()
        sys.setrecursionlimit(214748)
        self.data_wait_for_save = False
        self.dictionary = sbst()
        self.DB = DataBase(name)
        self.build_tree()

    # заполнение дерева из бд
    def build_tree(self):
        data = self.DB.get_from_db()
        if data != []:
            for a in data:
                self.dictionary.addfrom(a[0])
        self.update_datas.emit()

    # вставка элемента в дерево
    def insert_value(self, val):
        self.data_wait_for_save = True
        self.dictionary.add(val)
        self.update_datas.emit()

    # удаление элемента по ключу
    def delete_value(self, val):
        self.data_wait_for_save = True
        self.dictionary.remove(val)
        self.update_datas.emit()
     # обход дерева
    def bypass_tree(self):
        return self.dictionary.forward_from()

    def get_tree(self):
        logging.log(logging.INFO, "call get_tree")
        return self.dictionary.bp()

    # сохранение данных в базе
    def save_data(self):
        if self.data_wait_for_save:
            self.data_wait_for_save = False
            path = self.dictionary.bp()
            path.pop(0)
            self.DB.save_all(path)
            logging.log(logging.INFO, ' данные добавлены в бд')
        else:
            logging.log(logging.INFO, ' нет несохраненных данных')

    # загрузка данных из базы
    def load_data(self, parent):
        self.dictionary = sbst()
        self.build_tree()
        parent.draw_tree()
        logging.log(logging.INFO, ' данные успешно получены из бд')
        self.update_datas.emit()
    # удаление всех данных
    def del_all_from_tree(self):
        if self.dictionary.root is not None:
            self.data_wait_for_save = True
            self.dictionary = sbst()
        self.update_datas.emit()
