from typing import Any, List, Dict, Tuple, Set
import re
import csv
from teste import Teste


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
    dados.gerarColunasPorLinha()
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


class Logger():
    def __init__(self,fileName:str|None = None):
        self._filename : str

    def log(self,string:str):
        
        return
