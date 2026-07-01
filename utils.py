from typing import Any, List, Dict, Tuple
import re
import csv

class Teste():
    def __init__(self):
        numLinhas : int = -1
        numColunas : int = -1

        dados: List[List[float]] = []

        pesoColunas : Dict[int, int] = {}
        linhasPorColuna : Dict[int, List[int]] = {}
        colunasPorLinha : Dict[int, List[int]] = {}

    def gerarColunasPorLinha(self):
        lpc = self.getLinhasPorColunas()

        cpl = self.getColunasPorLinha()

        # inicializamos o dicionário
        for i in range(1,self.getNumLinhas()+1):
            key = int(i)
            value = []
            cpl.update({key:value})

        for coluna in lpc:
            linhas = lpc[coluna]
            for linha in linhas:
                cpl[int(linha)].append(int(coluna))

    def gerarLinhasPorColuna(self):
        temp = {}
        p = self.getDados()

        for i in p:
            key = i[0]
            value = i[2:]
            dic = {key:value}
            temp.update(dic)
        
        self.setLinhasPorColuna(temp)

    def gerarPesoColunas(self):
        temp = {}
        for d in self.dados:
            key : int = d[0]
            value : float = d[1]

            dic : Dict[int, float] = {key : value}
            temp.update(dic)

        self.setPesoColunas(temp)


    def __str__(self):
        bordaH : str = '-------------------------------------\n'

        nL : str = 'NUM LINHAS   : {self.numLinhas}\n'
        nC : str = 'NUM COLUNAS  : {self.numColunas}\n'

        p = self.getPesoColunas()
        pC : str = 'Peso Colunas\n'
        for i in p:
            key = str(i)
            value = str(p[i])
            s = f'> {key} : {value}\n'
            pC = pC + s

        l = self.getLinhasPorColunas()
        lPC : str = 'Linhas Por Colunas\n'
        for i in l:
            key = str(i)
            value = str(l[i])
            s = f'> {key} : {value}\n'
            lPC = lPC + s

        return bordaH + nL + nC + bordaH + pC + bordaH + lPC + bordaH

    def getNumLinhas(self) -> int:
        return self.numLinhas
    
    def getNumColunas(self) -> int:
        return self.numColunas
    
    def getDados(self) -> List[List[float]]:
        return self.dados
    
    def getPesoColunas(self) -> Dict[int, float]:
        return self.pesoColunas
    
    def getLinhasPorColunas(self) -> Dict[int, List[int]]:
        return self.linhasPorColuna
    
    def getColunasPorLinha(self) -> Dict[int, List[int]]:
        return self.colunasPorLinha

    def setNumLinhas(self, num):
        self.numLinhas = num

    def setNumColunas(self, num):
        self.numColunas = num

    def setDados(self, dados):
        self.dados = dados
    
    def setPesoColunas(self, pesos):
        self.pesoColunas = pesos

    def setLinhasPorColuna(self, lpc):
        self.linhasPorColuna = lpc

    def setColunasPorLinhas(self, cpl):
        self.colunasPorLinhas = cpl
        

def ExtrairMetadado(linha:str) -> Tuple[str, int]: 
    metadado : Tuple[str, int] = ("", -1)
    lin = re.search(r"LINHAS\s+(\d+)", linha) # type: ignore
    col = re.search(r"COLUNAS\s+(\d+)", linha) # type: ignore
    if lin:
        metadado = ('LINHAS', int(lin.group(1)))
    elif col:
        metadado = ('COLUNAS', int(col.group(1)))
    return metadado

def ExtraiDadosLinha(linha: str) -> List[float]:
    dadosLinha = []
    buffer = ""
    bufferFlag = False

    for c in linha:
        if c == " " or c == "\n":
            if bufferFlag:
                dadosLinha.append(float(buffer))
            buffer = ""
            bufferFlag = False
        else:
            buffer = buffer + c
            bufferFlag = True
    return dadosLinha

def ExtraiDados(file) -> Teste:
    dados : Teste = Teste()
    info = []
    index = 0

    while True:
        linha = file.readline()
        if linha == "":
            break
        else:
            index +=1
            if index == 1 or index == 2:
                meta = ExtrairMetadado(linha)
                if meta[0] == "LINHAS":
                    dados.setNumLinhas(meta[1])
                elif meta[0] == "COLUNAS":
                    dados.setNumColunas(meta[1])
            elif index > 3:
                dadosLinha : List[float]= ExtraiDadosLinha(linha)
                info.append(dadosLinha)
            else:
                continue
    dados.setDados(info)
    dados.gerarPesoColunas()
    dados.gerarLinhasPorColuna()
    return dados

def LerDados(caminho:str) -> Teste:
    dados : Teste
    with open(caminho, "+rt") as file:
        dados : Teste = ExtraiDados(file)

    return dados


# LEITURA DO ARQUIVO CSV PARA O BOXPLOT -------------------------------------

# estrutura do CSV
# +--------------+--------------------+-----------------------------------+
# |  instance ID |  valor-literatura  |  valores dos testes               |
# +--------------+--------------------+-----------------------------------+
# |              |                    |        |        |        |        |                               |
# |              |                    |        |        |        |        |
# |              |                    |        |        |        |        |
# |              |                    |        |        |        |        |
# +--------------+--------------------+-----------------------------------+

def _module(x:float) -> float:
    """
    retorna o módulo de x
    """
    return x if (x >= 0) else -x

def _ToDict(linha:List[str]) -> Dict[str, List[float]]:
    """
    Recebe uma *linha* de um arquivo CSV e o converte em um dicionário.
    O primeiro elemento de *linha* é considerado o ID da instância e os demais
    elementos como números inteiros representando o resultado de execucoes
    do algoritmo genetico
    """

    n:int = len(linha)
    instanceID:str = linha[0]
    referenceValue : float = float(linha[1])
    elems:List[float] = []

    for i in range(2, n):
        result : float = float(linha[i])
        percentual : float = _module((referenceValue - result)/referenceValue)
        elems.append(percentual)
    
    return {instanceID : elems}

def LerCSV(caminho:str) -> Dict[str, List[float]]:
    data : Dict[str, List[float]] = {}

    with open(caminho, newline='') as CSVfile:
        reader = csv.reader(CSVfile)
        for l in reader:
            data.update(_ToDict(l))
    
    return data
