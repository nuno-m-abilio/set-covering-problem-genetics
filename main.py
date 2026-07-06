import utils
from teste import Teste
from typing import List
from cromossomo import Cromossomo

from sys import argv

def main(caminho:str):
    print(f'CAMINHO : {caminho}')
    # ETAPA 0 : Leitura dos Dados
    dados : Teste = utils.LerDados(caminho)

    # ETAPA 1 : Geração da população inicial
    # a população inicial é uma lista de cromossomos
    # um cromossomo é um tipo de dado que armazena o a soma da solução e uma lista com os genes

    tamPop : int = 100
    dados.setTamPop(tamPop)
    dados.gerarPopulacaoInicial()
    
    PARADA = False
    iter = 0
    while not PARADA:
        if (iter % 100) == 0:
            print(iter)
        selecionados : List[Cromossomo] = dados.selecionarCromossomos()
        filho : Cromossomo = dados.cruzarCromossomos(selecionados)
        filho = dados.mutarCromossomo(filho,iter)
        #print(f'filho antes : {filho}')
        filho = dados.buscaLocal(filho)
        #print(f'filho depois : {filho}')

        pesoMenosApto:float = dados.getCustoMenosApto()
        pesoFilho:float = filho.getPeso()

        if pesoFilho < pesoMenosApto:
            dados.insereFilho(filho)
            iter += 1

        #novaPop : List[Cromossomo] = []
        #for _ in range(tamPop):
        #    filho : Cromossomo = dados.cruzarCromossomos(selecionados)
        #    novaPop.append(filho)

        #dados.atualizaPopulacao(novaPop)


        # ETAPA 2 : Avaliação
        # ETAPA 3 : Seleção
        # ETAPA 4 : Cruzamento
        # ETAPA 5 : Mutação
        # ETAPA 6 : Busca Local
        # ETAPA 7 : Atualização da População

        #iter += 1
        if iter == 501 : PARADA = True

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
