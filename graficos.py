import json
import matplotlib.pyplot as plt
import pandas as pd

from typing import List, Dict
from analise import Analise


# // auxiliares
def _getMelhorCusto(custos:List[float]) -> float:
    melhorCusto:float = float('inf')
    for custo in custos:
        if custo < melhorCusto:
            melhorCusto = custo
    return melhorCusto

# //

def analisesComparativas():
    # recuperamos as informações de população das configurações
    pops:List[int] = []
    with open('tests-config.json','r',encoding='utf8') as file:
        data = json.load(file)
        parametros = data['parametros']
        pops = parametros['tamanho-populacao']
        
    # criamos os objetos analise para cada populacao
    analises:Dict[int,Analise] = {}
    for pop in pops:
        analises.update({pop:Analise(pop)})

    
    # abrimos o arquivo json com os resultados dos testes
    with open('tests-results/test01.dat.json','r',encoding='utf8') as file:
        data:List[Dict] = json.load(file)

        for test in data:
            for _, testData in test.items():
                # recuperamos os valores
                tampop = testData['tamanho-populacao']
                taxaMin = testData['taxa-mutacao-minima']
                tempoMedio = testData['tempo-exec-medio']
                melhorCusto = _getMelhorCusto(testData['melhores-custos'])
                #print(f'melhorCusto : {melhorCusto}')
                numIter = testData['numero-iteracoes']

                # atualizamos o obejto
                analises[tampop].addTempo((tempoMedio,numIter))
                analises[tampop].addMelhor((melhorCusto,numIter))
                analises[tampop].addMelhorTaxa((melhorCusto,taxaMin))

    # construção dos gráficos
    # // tempo por iterações

    for pop, obj in analises.items():
        temposPorIter = obj.getTemposPorIter() # [(tempo,iter)]
        tempos = [v[0] for v in temposPorIter]
        iteracoes = [v[1] for v in temposPorIter]

        plt.plot(iteracoes, tempos, marker="o", label=f"População {pop}")

    plt.title("Tempo médio × Número de iterações")
    plt.xlabel("Número de iterações")
    plt.ylabel("Tempo médio de execução (s)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # construção dos gráficos
    # // qualidade por iterações

    for pop, obj in analises.items():
        custosPorIter = obj.getMelhoresPorIter() # [(melhor,iter)]
        #print(f'custosPorIter : {custosPorIter}')
        melhores = [v[0] for v in custosPorIter]
        iteracoes = [v[1] for v in custosPorIter]

        plt.plot(iteracoes, melhores, marker="o", label=f"População {pop}")

    plt.title("Melhores Custos × Número de iterações")
    plt.xlabel("Número de iterações")
    plt.ylabel("Melhor Custo")
    plt.grid(True)
    plt.legend()
    plt.show()

    # // qualidade por taxa de mutacao
    for pop, obj in analises.items():
        custosPorTaxa = obj.getMelhoresPorTaxa() # [(melhor,taxa)]
        #print(f'custosPorIter : {custosPorIter}')
        melhores = [v[0] for v in custosPorTaxa]
        taxas = [v[1] for v in custosPorTaxa]

        plt.plot(taxas, melhores, marker="o", label=f"População {pop}")

    plt.title("Melhores Custos × Taxas de mutacao")
    plt.xlabel("Taxas de mutacao")
    plt.ylabel("Melhor Custo")
    plt.grid(True)
    plt.legend()
    plt.show()

    return

def boxPlot():
    """
    """
    print('boxPlot()\n')
    # para cada caso de teste devemos pegar os resultados das 10 execuções e calcular o GAP
    # o boxplot é dos valores do GAP

    casosTeste:List[str] = ['test01','test02','test03','test04','test05','wren01','wren02','wren03','wren04',]

    valoresReferencia:Dict
    with open('referencia.json','r',encoding='utf8') as file:
        valoresReferencia = json.load(file)

    resultadosExecucoes:Dict = {}
    for teste in casosTeste:
        path:str = 'tests-results/' + teste + '.dat.json'

        with open(path,'r',encoding='utf8') as file:
            resultado:Dict = json.load(file)[0]
            for _, value in resultado.items():
                resultadosExecucoes.update({teste:value['melhores-custos']})

    # estrutura de dados
    # .. um dicionário em que a chave é o nome do caso de teste e o valor é a lista com os GAPS

    # inicialização da estrutura de dados
    boxes:List[List] = []
    labels:List[str] = []
    data:Dict = {}
    for caso in casosTeste:
        # recuperamos o valor referência para o caso de teste
        valorRef:float = valoresReferencia[caso]

        gaps:List[float] = []
        results:List[float] = resultadosExecucoes[caso]

        # calculamos todos os gaps para os valores dos resultados e adicionamos na lsita de gaps
        for res in results:
            gap:float = (res - valorRef)/valorRef
            gaps.append(gap)

        data.update({caso:gaps})

    for caso, res in data.items():
        boxes.append(res)
        labels.append(caso)

    plt.boxplot(boxes,tick_labels=labels)
    plt.show()

    return

def tabelaComparativa():
    # Exemplo de dados
    casosTeste:List[str] = ['test01','test02','test03','test04','test05','wren01','wren02','wren03','wren04',]

    valoresReferencia:Dict
    with open('referencia.json','r',encoding='utf8') as file:
        valoresReferencia = json.load(file)

    temposExecucoes:Dict = {}
    resultadosExecucoes:Dict = {}
    for teste in casosTeste:
        path:str = 'tests-results/' + teste + '.dat.json'

        with open(path,'r',encoding='utf8') as file:
            resultado:Dict = json.load(file)[0]
            for _, value in resultado.items():
                resultadosExecucoes.update({teste:value['melhores-custos']})
                temposExecucoes.update({teste:value['tempos-execucao']})

    # estrutura de dados
    # .. um dicionário em que a chave é o nome do caso de teste e o valor é a lista com os GAPS

    # inicialização da estrutura de dados
    boxes:List[List] = []
    labels:List[str] = []
    data:Dict = {}
    gaps:List[float] = []
    for caso in casosTeste:
        # recuperamos o valor referência para o caso de teste
        valorRef:float = valoresReferencia[caso]

        gaps:List[float] = []
        results:List[float] = resultadosExecucoes[caso]

        # calculamos todos os gaps para os valores dos resultados e adicionamos na lsita de gaps
        for res in results:
            gap:float = (res - valorRef)/valorRef
            gaps.append(gap)

        data.update({caso:gaps})

    for caso, res in data.items():
        boxes.append(res)
        labels.append(caso)

    plt.boxplot(boxes,tick_labels=labels)
    plt.show()

    novoGap = 0.0
    novoGaps = []
    indexMelhorCusto:int = -1
    melhoresSolucoes:List[float] = []
    temposMelhoresSolucoes:List[float] = []
    for test, res in resultadosExecucoes.items():
        melhorCusto = _getMelhorCusto(res)
        novoGap = (melhorCusto - valoresReferencia[test])/valoresReferencia[test]
        novoGaps.append(novoGap)
        indexMelhorCusto = res.index(melhorCusto)
        tempo = temposExecucoes[test][indexMelhorCusto]
        melhoresSolucoes.append(melhorCusto)
        temposMelhoresSolucoes.append(tempo)


    print(f'Problema = {len(casosTeste)}')
    print(f'Melhor Solução = {len(melhoresSolucoes)}')
    print(f'GAPS = {len(novoGaps)}')
    print(f'Tempos = {len(temposMelhoresSolucoes)}')
    
    dados = {
        "Problema": casosTeste,
        "Melhor Solução": melhoresSolucoes,
        "GAP": novoGaps,
        "Tempo de execução": temposMelhoresSolucoes
    }

    df = pd.DataFrame(dados)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("tight")
    ax.axis("off")

    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center"
    )

    plt.show()

    return

if __name__ == "__main__":
    boxPlot()
    tabelaComparativa()