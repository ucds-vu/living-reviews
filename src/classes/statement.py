from imports import *

class Statement:
    def __init__(self, statement, study):
        self.statement = statement.replace(" ", "+")
        self.statement = self.statement.replace('"','')
        self.study = study
