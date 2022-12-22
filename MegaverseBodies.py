from abc import ABC, abstractmethod

class MegaverseBody(ABC):
    def __init__(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

    @abstractmethod
    def getParams(self, candidateId):
        return {}

    @staticmethod
    def getUrl():
        return "https://challenge.crossmint.io/api"


class Polyanet(MegaverseBody):
    def __init__(self):
        MegaverseBody.__init__(self)

    def getParams(self, candidateId):
        return {"row": self.row_idx, "column": self.col_idx, "candidateId": candidateId}

    @staticmethod
    def getUrl():
        return MegaverseBody.getUrl() + "/polyanets"

class Cometh(MegaverseBody):
    def __init__(self, direction):
        MegaverseBody.__init__(self)
        self.direction = direction

    def getParams(self, candidateId):
        return {"row": self.row_idx, "column": self.col_idx, "direction": self.direction, "candidateId": candidateId}

    @staticmethod
    def getUrl():
        return MegaverseBody.getUrl() + "/comeths"

class Soloon(MegaverseBody):
    def __init__(self, color):
        MegaverseBody.__init__(self)
        self.color = color

    def getParams(self, candidateId):
        return {"row": self.row_idx, "column": self.col_idx, "color": self.color, "candidateId": candidateId}

    @staticmethod
    def getUrl():
        return MegaverseBody.getUrl() + "/soloons"