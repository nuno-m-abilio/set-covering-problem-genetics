import utils
from teste import Teste
from typing import List
from cromossomo import Cromossomo

from sys import argv

def main(caminho:str):
    # ETAPA 0 : Leitura dos Dados
    dados : Teste = utils.LerDados(caminho)
    #print('DADOS')
    #print(dados)

    tamPop : int = 10000

    dados.setTamPop(tamPop)
    dados.gerarPopulacaoInicial()
    #dados.exibirPopAtual()
    #print('\n\nSELECIONADOS')

    # ETAPA 1 : Geração da população inicial
    # a população inicial é uma lista de cromossomos
    # um cromossomo é um tipo de dado que armazena o a soma da solução e uma lista com os genes
    
    PARADA = True
    iter = 0
    while not PARADA:
        print(f'iter {iter}')
        selecionados : List[Cromossomo] = dados.selecionarCromossomos()

        novaPop : List[Cromossomo] = []
        for _ in range(tamPop):
            filho : Cromossomo = dados.cruzarCromossomos(selecionados)
            novaPop.append(filho)

        dados.atualizaPopulacao(novaPop)


        # ETAPA 2 : Avaliação
        # ETAPA 3 : Seleção
        # ETAPA 4 : Cruzamento
        # ETAPA 5 : Mutação
        # ETAPA 6 : Busca Local
        # ETAPA 7 : Atualização da População

        iter += 1
        if iter == 1000: PARADA = True

    print('FIM')
    print(dados.getSolucao())
    if dados.validarSolucao():
        print('SOLUÇÃO VÁLIDA')
    else:
        print('SOLUÇÃO INVÁLIDA')
        print(f'LINHAS DESCOBERTAS : {dados.getLinhasDescobertas()}')
        print(dados)



if __name__ == "__main__":
    if len(argv) == 1:
        print("ERROR : Missing argument file path")
    else:
        main(argv[1])
