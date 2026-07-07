import utils
from teste import Teste
from typing import List
from cromossomo import Cromossomo
from execution import Execution
from time import time

from sys import argv

def run(obj:Execution,i:int) -> Execution:
    # ETAPA 0 : Leitura dos Dados
    dados:Teste = utils.LerDados(obj.getPath())

    # setamos as variáveis
    dados.setTamPop(obj.getTamPop())
    dados.setTaxaMutMin(obj.getMinMutRate())

    maxIter:int = obj.getNumIter()

    # ETAPA 1 : Geração da população inicial
    # a população inicial é uma lista de cromossomos
    # um cromossomo é um tipo de dado que armazena o a soma da solução e uma lista com os genes
    t0:float = time()
    dados.gerarPopulacaoInicial()
    
    counter = 0
    iter = 0
    while (iter <= maxIter):
        counter += 1
        # ETAPA 2 : Seleção dos reprodutores por torneio
        selecionados:List[Cromossomo] = dados.selecionarCromossomos()

        # ETAPA 3 : Cruzamento dos reprodutores selecionados
        filho:Cromossomo = dados.cruzarCromossomos(selecionados)

        # ETAPA 4 : Mutacao do cromossomo filho
        filho = dados.mutarCromossomo(filho,iter)

        # ETAPA 5 : Melhoramento do filho por busca-local
        filho = dados.buscaLocal(filho)

        # ETAPA 6 : Atualizamos a população
        if dados.atualizaPopulacao(filho):
            iter += 1
            counter = 0

        if counter >= maxIter/4:
            break

    tf:float = time()
    
    custoMaisApto:float = dados.getCustoMaisApto()
    tempoExecucao:float = tf - t0

    if dados.validarSolucao():
        print(f'SOLUÇÃO VÁLIDA #{i}')
    else:
        print('SOLUÇÃO INVÁLIDA')
        print(f'LINHAS DESCOBERTAS : {dados.getLinhasDescobertas()}')
        print(dados)

    obj.addCost(custoMaisApto)
    obj.addTime(tempoExecucao)

    return obj