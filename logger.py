from cell_map import CellMap
from typing import List
from serialization import serialize_cellmap, serialize_cellmap_only


class Logger:
    def __init__(self, session: str = 'default', path: str = 'logs'):
        self.session = session
        self.path = path
        self.id = 0
        self.count = 1


    def get_file_name(self) -> str:
        return '{0}/{1}_{2}.log'.format(self.session, self.count, self.path)


    def log(self, cellmap: List[List[int]]):
        serialize_cellmap_only(cellmap, len(cellmap[0]), len(cellmap), self.get_file_name())
        self.count += 1


    def start_session(self, cellmap: List[List[int]], session_name: str = ''):
        if session_name == '':
            self.id += 1
            self.session = 'default_' + str(self.id)
        else:
            self.session = session_name

        serialize_cellmap(cellmap, self.get_file_name())

        self.count = 1


    def end_session(self):
        self.session = 'default'
        self.count = 1
