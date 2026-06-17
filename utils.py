from typing import List, Dict
import csv


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

def ExtraiDados(file) -> List[List[float]]:
    dados = []
    numLinhas = 0

    while True:
        linha = file.readline()
        if linha == "":
            break
        else:
            numLinhas +=1
            if numLinhas > 3:
                dadosLinha : List[float]= ExtraiDadosLinha(linha)
                dados.append(dadosLinha)
    return dados

def LerDados(caminho:str) -> List[List[float]]:
    dados = [[0.0]]
    with open(caminho, "+rt") as file:
        dados : List[List[float]] = ExtraiDados(file)

    return dados


# LEITURA DO ARQUIVO CSV PARA O BOXPLOT -------------------------------------

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
