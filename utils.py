from typing import List

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
