from typing import List
from functools import reduce
import json

class Execution():
    def __init__(self,name:str):
        self.diretorio:str
        self.fileName:str = name
        self.numExecucoes:int = 0

        # parametros
        self.tamPop:int
        self.minMutRate:float
        self.numIter:int

        # resultados
        self.betterCosts:List[float] = []
        self.execTimes:List[float] = []
        self.averageExecTime:float = 0.0
        
        with open('tests-results/'+self.fileName+'.json','w',encoding='utf8') as file:
            json.dump([],file,indent=4,ensure_ascii=False)


    def refresh(self):
        self.numExecucoes = 0
        self.betterCosts = []
        self.execTimes = []
        self.averageExecTime = 0.0
        return

    def dump(self,id:int):
        """
        Escreve as informações em um arquivo json
        """
        self.averageExecTime = reduce(lambda x, y : x + y, self.execTimes) / len(self.execTimes)
        path:str = 'tests-results/' + self.fileName + '.json'

        content = {
            "teste" : self.fileName,
            "num-execucoes" : self.numExecucoes,
            "tamanho-populacao" : self.tamPop,
            "taxa-mutacao-minima" : self.minMutRate,
            "numero-iteracoes" : self.numIter,
            "melhores-custos" : self.betterCosts,
            "tempos-execucao" : self.execTimes,
            "tempo-exec-medio" : self.averageExecTime
        }

        with open(path,'r',encoding='utf8') as file:
            data = json.load(file)
            data.append({f'test#{id}' : content})
            
        with open(path,'w',encoding='utf8') as file:
            json.dump(data,file,indent=4,ensure_ascii=False)

        return
    
    def addExecution(self):
        self.numExecucoes += 1
        return
    
    def addCost(self,cost:float):
        self.betterCosts.append(cost)
        return

    def addTime(self,execTime:float):
        self.execTimes.append(execTime)
        return

    def getPath(self) -> str:
        """
        Monta o caminho do arquivo de dados e o retorna
        """
        return self.diretorio + self.fileName

    def setParams(self,dir:str,name:str,tampop:int,minrate:float,numiter:int):
        self.diretorio = dir
        self.fileName = name
        self.tamPop = tampop
        self.minMutRate = minrate
        self.numIter = numiter
        return
    
    # // default getters and setters

    def getFileName(self) -> str:
        return self.fileName

    def getTamPop(self) -> int:
        return self.tamPop
    
    def getMinMutRate(self) -> float:
        return self.minMutRate
    
    def getNumIter(self) -> int:
        return self.numIter
     