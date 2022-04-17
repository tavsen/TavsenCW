import logging
import sys

from DB_AA import DataBase
from AA import sbst


class Facade:
    def __init__(self, name='Tree_data.db'):
        sys.setrecursionlimit(31)
        self.data_wait_for_save = False
        self.and_and = sbst()
        self.DB = DataBase(name)

    def add_value(self, val):
        self.data_wait_for_save = True
        self.and_and.add(val)

    def remove_value(self, val):
        self.data_wait_for_save = True
        self.and_and = self.and_and.remove(val)

    def bypass_tree(self, val):
        return self.and_and.forward_from(val)

    def save_data(self):
        if self.data_wait_for_save:
            self.data_wait_for_save = False
            path = self.and_and.forward_from(0)
            self.DB.save_all(path)
            logging.log(logging.INFO, ' Data added to DB')
        else:
            logging.log(logging.INFO, ' There is no unsaved Data')
