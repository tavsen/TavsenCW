import logging
import sys

from DB_AA import DataBase
from AA import sbst


class Facade:
    """
    Класс фасада (шаблона проектирования)
    """
    def __init__(self, name='Tree_data.db'):
        """
        создание объекта базы данных, структуры данных и запись элементов из БД в структуру данных (функция build_tree).
        data_wait_for_save - False, если нет данных для сохранения, True, если есть данные для сохранения
        :param name: имя базы данных
        """
        sys.setrecursionlimit(31)    # максимальное кол-во рекурсий 2147483647
        self.data_wait_for_save = False
        self.dictionary = sbst()  # тут будет первый элемент
        self.DB = DataBase(name)
        self.build_tree()

    def build_tree(self):
        """
        запись элементов из БД в структуру данных
        :return: None
        """
        data = self.DB.get_from_db()
        if data != []:
            for a in data:
                self.dictionary.add(2)

    def add_value(self, val):
        """
        Вставка элементов в структуру данных
        :param val: данные для вставки
        :return: None
        """
        self.data_wait_for_save = True
        self.dictionary.add(val)

    def remove_value(self, val):
        """
        Удаление данных из структуры данных
        :param key: ключ, по которому нужно найти объект и удалить его
        :return: None
        """
        self.data_wait_for_save = True
        self.dictionary = self.dictionary.remove(val)


    def bypass_tree(self,val):
        """
        Вызывает функцию обхода дерева
        :return: возвращает путь обхода, а на первом месте максимальная глубина дерева
        """
        return self.dictionary.forward_from(val)

    def save_data(self):
        """
        Если есть несохраненные данные (data_wait_for_save==True), тогда в БД записываются новые данные
        :return: None
        """
        if self.data_wait_for_save:
            self.data_wait_for_save = False
            path = self.dictionary.forward_from(0, [0])
            path.pop(0)
            self.DB.save_all(path)
            logging.log(logging.INFO, ' данные добавлены в бд')
        else:
            logging.log(logging.INFO, ' нет несохраненных данных')

    def del_all_from_bst(self):
        """
        если в дереве есть хоть один ключ, тогда все данные в дереве удаляются
        :return: None
        """
        if self.dictionary.val is not None:
            self.data_wait_for_save = True
            self.dictionary = sbst()