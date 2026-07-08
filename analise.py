from typing import List, Tuple

class Analise():
    def __init__(self,pop:int):
        self.tamPop:int = pop
        self.tempoPorIter:List = []
        self.melhorPorIter:List = []
        self.melhorPorTaxa:List = []

    def addTempo(self,tempo:Tuple[float,int]):
        self.tempoPorIter.append(tempo)
        return
    
    def addMelhor(self,melhor:Tuple[float,int]):
        self.melhorPorIter.append(melhor)
        return
    
    def addMelhorTaxa(self,melhor:Tuple[float,int]):
        self.melhorPorTaxa.append(melhor)
        return
    
    # // default getters and setters
    def getTemposPorIter(self) -> List[Tuple[float,int]]:
        return self.tempoPorIter
    
    def getMelhoresPorIter(self) -> List[Tuple[float,int]]:
        return self.melhorPorIter
    
    def getMelhoresPorTaxa(self) -> List[Tuple[float,float]]:
        return self.melhorPorTaxa

    def setTamPop(self,tam:int):
        self.tamPop = tam
        return
    