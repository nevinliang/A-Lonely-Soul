import os
path = os.path.dirname(__file__)


class Files:
    @staticmethod
    def read(name):
        file = os.path.join(path, 'sentences.txt')
        file = open(file, "r")
        lines = file.readlines()
        file.close()
        return lines
