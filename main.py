from typing import Dict, List
from execution import Execution
from source import run
import json

def main():
    # lemos o arquivo de configuração dos casos de teste
    with open('tests-config.json','r',encoding='utf-8') as file:
        testsConfig:Dict = json.load(file)

    diretorio:str = testsConfig["diretorio"]
    arquivosTeste:List[str] = testsConfig["testes"]
    execucoes:int = testsConfig['execucoes']

    # parametros
    parametros = testsConfig['parametros']
    tamanhoPopulacao:List[int] = parametros['tamanho-populacao']
    taxaMutMinima:List[float] = parametros['taxa-mutacao-minima']
    numeroIteracoes:List[int] = parametros['numero-iteracoes']

    # para cada execução do algoritmo, queremos armazenar o tempo que levou para concluir
    # o custo da melhor solução encontrada
    
    i:int = 0
    counter:int = 0
    for teste in arquivosTeste:
        bateria:Execution = Execution(teste)
        for pop in tamanhoPopulacao:
            for taxa in taxaMutMinima:
                for numIter in numeroIteracoes:
                    bateria.setParams(diretorio,teste,pop,taxa,numIter)
                    for _ in range(execucoes):
                        bateria.addExecution()
                        bateria = run(bateria,i)
                        i += 1

                    print('\n')
                    bateria.dump(counter)
                    bateria.refresh()
                    counter += 1
    return

if __name__ == "__main__":
    main()
