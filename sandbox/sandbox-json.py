import json
from typing import List

def main():
    with open('tests-config.json','r',encoding='utf8') as file:
        dados = json.load(file)

        diretorio:str = dados["diretorio"]
        arquivosTeste:List[str] = dados["testes"]
        execucoes:int = dados['execucoes']

        # parametros
        parametros = dados['parametros']
        tamanhoPopulacao:List[int] = parametros['tamanho-populacao']
        taxaMutMinima:List[float] = parametros['taxa-mutacao-minima']
        numeroIteracoes:List[int] = parametros['numero-iteracoes']

        print(f'diretorio           : {diretorio}')
        print(f'testes              : {arquivosTeste}')
        print(f'execucoes           : {execucoes}')
        print(f'tamanho-populacao   : {tamanhoPopulacao}')
        print(f'taxa-mutacao-minima : {taxaMutMinima}')
        print(f'numero-iteracoes    : {numeroIteracoes}')
    return

if __name__ == "__main__":
    main()