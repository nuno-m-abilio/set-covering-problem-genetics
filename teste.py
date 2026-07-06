from typing import Any, List, Dict, Tuple, Set
from dataclasses import dataclass
from cromossomo import Cromossomo
from functools import reduce
import re
import csv
import random
import bisect
from math import exp

class Teste():
    # ----- ATRIBUTOS -----
    # pesoColunas     : dicionario {coluna : peso}
    # linhasPorColuna : dicionario {coluna : [linhas cobertas]}
    # colunasPorLinha : dicionário {linha : [colunas cobertas]}
    # populacaoAtual  : lista de CROMOSSOMOS
    # populacaoFutura : lista de CROMOSSOMOS

    def __init__(self):
        self.numLinhas : int = -1
        self._linhas:List[int] = []

        self.numColunas : int = -1
        self._colunas:List[int] = []

        self.tamPop:int
        self._taxaMutacaoMinima:float = 1

        self.dados: List[List[float]] = []               # linhas do documento de texto

        self.pesoColunas : Dict[int, float] = {}           # {colunaID : peso}
        #self.linhasPorColuna : Dict[int, List[int]] = {} # {colunaID : [linhas cobertas pela coluna]}
        #self.colunasPorLinha : Dict[int, List[int]] = {} # {linhaID : [colunas cobertas pela linha]}

        self._linhasPorColuna : Dict[int, Set] = {}
        self._colunasPorLinha : Dict[int, Set] = {}

        self._populacaoAtual : List[Cromossomo] = []
        self._populacaoRankeada : List[Cromossomo] = []

        self._linhasDescobertas : Set[int] = set()


    # ------ API ---------
    # lerDados()               -> Dados filtrados
    # gerarPopulacaoInicial()  -> Cromossomos da população inicial
    # selecionarCromossomos()  -> Lista de cromossomos reprodutores
    # cruzarCromossomos()      -> Filhos dos cromossomos reproduzidos
    # mutarCromossomo()         -> Muta a população futura
    # buscaLocal()             -> 
    # atualizaPopulacao()      -> Atualiza a população
    # getSolucao()             -> Retorna o melhor individuo gerado
    
    def gerarPopulacaoInicial(self):
        """
        Gera a população inicial de cromossomos ordenados em ordem de qualidade, da pior para a melhor
        """
        numCromossomosGerados = 0
        while numCromossomosGerados <= self.tamPop:
            # geramos um individuo
            individuo : Cromossomo = self._gerarIndividuo()
            ehSol : bool = self.validarSolucao(individuo)

            if not ehSol:
                print("ERRO : Solucao Inválida Gerada")

            # adicionamos o individuo à população - mantendo a ordem
            self._insereIndividuo(individuo)
            numCromossomosGerados += 1
        return
    
    def selecionarCromossomos(self) -> List[Cromossomo]:
        self._rankearCromossomos()
        pai, mae = self._sortear()
        return [pai,mae]
    
    def cruzarCromossomos(self,casal:List[Cromossomo]) -> Cromossomo:
        filho : Cromossomo = Cromossomo()
        genesPai = casal[0].getGenes()
        genesMae = casal[1].getGenes()

        genesFilho : Set[int] = genesPai | genesMae
        
        filho.setGenes(genesFilho)
        redundanciasFilho : List[int] = self._calcularRedundancias(genesFilho)
        filho.setRedundancias(redundanciasFilho)
        self._eliminarRedundancias(filho)
        filho.avaliarQualidade(self.pesoColunas)

        return filho
    
    def mutarCromossomo(self,indiv:Cromossomo,iter:int) -> Cromossomo:
        """
        Muta os genes de *indiv* de forma aleatória
        """
        mutado:Cromossomo = indiv

        taxaMutacao:float = self._calcTaxaMutacao()
        p:float = random.uniform(0.0,1.0)

        if p < taxaMutacao:
            mutado = self._mutar(indiv)

        return mutado

    def buscaLocal(self,indiv:Cromossomo) -> Cromossomo:
        #print('busca-local')
        primeiraMelhoria:Cromossomo = indiv

        genes:Set[int] = indiv.getGenes().copy()
        #print(f'genes = {genes}')
        colunasDisponiveis:Set[int] = set(self._colunas) - genes
        #print(f'colunas-disponiveis = {colunasDisponiveis}')

        PARAR = False
        while not PARAR:
            #colunasDisponiveis = colunasD
            for coluna in colunasDisponiveis:
                #print(f'coluna = {coluna}')
                removidas:Set[int] = set()
                pesoColuna:float = self.getPesoDaColuna(coluna)
                linhasCobertas:Set[int] = self.getLinhasDaColuna(coluna)
        
                for gene in genes:
                    #print(f'coluna {coluna} | gene {gene}')
                    pesoGene:float = self.getPesoDaColuna(gene)
                    linhasGene:Set[int] = self.getLinhasDaColuna(gene)
                    #print(f'linhas{gene} = {linhasGene}')
                    #print(f'linhasCobertas = {linhasCobertas}')
                    intersec:Set[int] = linhasCobertas & linhasGene
                    #print(f'intersec = {intersec}')

                    if len(linhasGene-intersec)==0 and pesoColuna < pesoGene:
                        #colunasD.remove(coluna)
                        genes.add(coluna)
                        genes.remove(gene)
                        removidas.add(gene)
                        #print('\n AHHHHH \n')
                        #print(f'removido = {gene}')
                        #print(f'adicionado = {coluna}')

                #print(f'removidas = {removidas}')
                if len(removidas) != 0:
                    primeiraMelhoria.setGenes(genes)
                    primeiraMelhoria.setRedundancias(self._calcularRedundancias(genes))
                    self._eliminarRedundancias(primeiraMelhoria)
                    primeiraMelhoria.avaliarQualidade(self.pesoColunas)
                    #colunasD = colunasD | removidas
                    #print(f'colunas-disponiveis = {colunasDisponiveis}')

                #colunasD.remove(coluna)

            PARAR = True

        #print('\n -------------------------------------- \n')


        return primeiraMelhoria

    def atualizaPopulacao(self,novaPop:List[Cromossomo]):
        self._populacaoAtual : List[Cromossomo]= []
        for individuo in novaPop:
            self._insereIndividuo(individuo)
        return

    def insereFilho(self,filho:Cromossomo):
        """
        Remove a individuo menos apto da populacao e insere *filho*
        """
        removido:Cromossomo = self._populacaoAtual.pop(0)
        self._insereIndividuo(filho)
        return

    def getSolucao(self) -> Cromossomo:
        return self._populacaoAtual[-1]

    def validarSolucao(self,individuo:Cromossomo|None = None) -> bool:
        solucao : Set[int]
        self._linhasDescobertas : Set[int] = set()

        if individuo is not None:
            solucao : Set[int] = individuo.getGenes()
        else:
            solucao : Set[int] = self.getSolucao().getGenes()

        vetorValidacao : List[bool] = [False]*(self.getNumLinhas() + 1)
        vetorValidacao[0] = True

        for coluna in solucao:
            linhas : Set[int] = self.getLinhasDaColuna(coluna)
            for linha in linhas:
                vetorValidacao[linha] = True

        for i in range(1,self.numLinhas+1):
            if not vetorValidacao[i]:
                self._linhasDescobertas.add(i)

        resultado : bool = reduce(lambda x, y : x and y, vetorValidacao)

        return resultado



    # ---- FUNÇÕES AUXILIARES ------
    # <gerarPopulacaoInicial()>
    # _gerarIndividuo()                   -> gera um cromossomo
    # _insereIndividuo(cromossomo)        -> insere um cromossomo na população em ordem de qualidade
    # _melhorColuna(colunas,linhasDescobertas) -> descobre a coluna que cobre o maior número de colunas descobertas

    def _gerarIndividuo(self) -> Cromossomo:
        genesEscolhidos : Set = set()                                         # conjunto das colunas que compõem a solução
        linhasDescobertas : Set = set([i for i in range(1,self.numLinhas+1)]) # conjunto das linhas descobertas
        coberturaPorLinha : List[int] = [0] * (self.numLinhas + 1)                   # vetor com o número de colunas que cobrem cada linha i

        while not (len(linhasDescobertas)==0):
            # selecionamos uma linha i aleatoriamente das linhasDescobertas
            linha : int = random.choice(list(linhasDescobertas))
            
            # pegamos o conjunto de colunas que cobrem a *linha*
            colunasQueCobrem : Set = self._colunasPorLinha[linha]

            # slecionamos a coluna j que cobre o maior número de linhas descobertas incluindo a *linha*
            melhorColuna : int = self._melhorColuna(colunasQueCobrem,linhasDescobertas,linha=linha)

            linhasDescobertas.remove(linha)
            
            if melhorColuna != 0:
                # conjunto das linhas cobertas pela melhor coluna
                linhasCobertas : Set = self._linhasPorColuna[melhorColuna]

                # conjunto das colunas que farão parte da solução
                genesEscolhidos = genesEscolhidos | {melhorColuna}

                # calculamos as redundancias
                for line in self._linhasPorColuna[melhorColuna]:
                    coberturaPorLinha[line] += 1

                linhasDescobertas = linhasDescobertas - linhasCobertas
            else:
                print(f'ERRO _melhorColuna() = 0  com linha = {linha}')
        
        individuo : Cromossomo = Cromossomo(genesEscolhidos)
        individuo.setRedundancias(coberturaPorLinha)
        self._eliminarRedundancias(individuo)
        individuo.avaliarQualidade(self.pesoColunas)

        return individuo

    def _melhorColuna(self,colunas:Set[int],linhasDescobertas:Set[int],linha:int|None=None, ) -> int:
        melhorColuna = 0
        melhorIndice = float('inf')   
        melhorCustoPorLinha : float = float('inf') 

        if linha is not None:
            # colunas que cobrem a linha
            colunasQueCobrem : Set[int] = self.getColunasDaLinha(linha)

            if len(colunasQueCobrem) == 0:
                print(f'\n 0 Colunas Cobrem a Linha {linha}')
            else:
                # calculamos a taxa de cobertura de cada coluna
                for col in colunasQueCobrem:
                    custoPorLinha : float = self._taxaCobertura(col,linhasDescobertas)
                    
                    if custoPorLinha < melhorCustoPorLinha:
                        melhorColuna = col

        else:
            for coluna in colunas:
                custoColuna : float = self.pesoColunas[coluna]
                linhasCobertas : Set = self._linhasPorColuna[coluna]
                intersecao : Set = linhasCobertas & linhasDescobertas

                norma = len(intersecao)
                indice = melhorIndice
                if norma != 0:
                    indice : float = custoColuna / len(intersecao)

                if indice < melhorIndice:
                    melhorColuna = coluna
                    melhorIndice = indice

        return melhorColuna

    def _taxaCobertura(self,coluna:int,linhasDescobertas:Set[int]) -> float:
        """
        Calcula a taxa de cobertura da *coluna* sobre as *linhasDescobertas*
        O resultado nunca será zero porque a coluna sempre cobrirá pelo menos 1 linha (verificação enterior necessária)
        """
        pesoColuna : float = self.getPesoDaColuna(coluna)
        linhasCobertas : Set[int] = self.getLinhasDaColuna(coluna)
        cobertura : Set[int] = linhasCobertas & linhasDescobertas
        normaCobertura : int = len(cobertura) # deve ser pelo menos '

        taxaCobertura = pesoColuna / normaCobertura
        return taxaCobertura

    def _insereIndividuo(self,individuo:Cromossomo):
        """
        Insere um *individuo* na população em ordem decrescente de qualidade
        os piores individuos ficam no começo
        """
        pesos = [-ind.getPeso() for ind in self._populacaoAtual]
        posicao = bisect.bisect(pesos,-individuo.getPeso())
        self._populacaoAtual.insert(posicao,individuo)
        return
    
    def _calcularRedundancias(self,genes:Set[int]) -> List[int]:
        redundancias = [0] * (self.numLinhas + 1)

        for gene in genes:
            linhas = self.getLinhasDaColuna(gene)
            for linha in linhas:
                redundancias[linha] += 1
        return redundancias

    def _eliminarRedundancias(self,individuo:Cromossomo):
        temp : Set[int] = individuo.getGenes().copy()

        while len(temp) != 0:
            # escolhemos uma coluna aleatória
            coluna : int = random.choice(list(temp))
            temp.remove(coluna)

            linhas : Set[int] = self._linhasPorColuna[coluna]

            if individuo.ehRedundante(linhas):
                individuo.removeGene(coluna,linhas) # já atualiza das redundâncias

        return

    # ---- FUNÇÕES AUXILIARES ------
    # <selecionarCromossomos()>
    # _rankearCromossomos()
    # _insereRankeado()
    # _sortear()

    def _rankearCromossomos(self):
        tamPop = self.tamPop
        termo = tamPop*(tamPop + 1)

        for i in range(len(self._populacaoAtual)):
            k = i + 1
            prob = 2*k / termo
            self._populacaoAtual[i].setProbabilidade(prob)
            self._insereRankeado(self._populacaoAtual[i])
        return
    
    def _insereRankeado(self,individuo:Cromossomo):
        probabilidades = [ind.getProbabilidade() for ind in self._populacaoRankeada]
        posicao = bisect.bisect(probabilidades,individuo.getProbabilidade())
        self._populacaoRankeada.insert(posicao,individuo)
        return

    def _sortear(self):
        candidatos = self._populacaoRankeada.copy()
        probs : List[float] = [ind.getProbabilidade() for ind in self._populacaoRankeada]
        pai, mae = random.choices(candidatos,probs,k=2)
        return pai, mae

    def gerarColunasPorLinha(self):
        # inicializamos o dicionario
        for i in range(1,self.getNumLinhas()+1):
            key = int(i)
            value = set()
            self._colunasPorLinha.update({key:value})

        for coluna in self._linhasPorColuna:
            linhas = self._linhasPorColuna[coluna]
            for linha in linhas:
                self._colunasPorLinha[int(linha)].update({int(coluna)})
        
        return

    def gerarLinhasPorColuna(self):
        temp = {}
        p = self.getDados()

        for i in p:
            key = int(i[0])
            value = i[2:]
            value = set(map(lambda x : int(x),value))
            dic = {key:value}
            temp.update(dic)
        
        self.setLinhasPorColuna(temp)

    def gerarPesoColunas(self):
        temp = {}
        for d in self.dados:
            key : int = int(d[0])
            value : float = d[1]

            dic : Dict[int, float] = {key : value}
            temp.update(dic)

        self.setPesoColunas(temp)

    # ////

    def _calcTaxaMutacao(self) -> float:
        """
        Calcula a taxa de mutacao variavel
        """
        custoMenosApto:float = self.getCustoMenosApto()
        custoMaisApto:float = self.getCustoMaisApto()
        expoente:float = -(custoMenosApto - custoMaisApto)/custoMenosApto
        taxa:float = self._taxaMutacaoMinima /(1-exp(expoente))
        return taxa

    def _mutar(self,indiv:Cromossomo) -> Cromossomo:
        mutado:Cromossomo = Cromossomo()

        genes:Set[int] = indiv.getGenes().copy()

        colunas:List[int] = []
        for i in range(1,self.numColunas+1):
            colunas.append(i)

        tam:int = len(genes)

        # selecionamos aleatoriamente um numero real entre 0 e 1
        num:float = random.uniform(0.0,1.0)
        teto:int = int(num*tam) + 1

        for _ in range(1,teto):
            col:int = random.choice(colunas)
            colunas.remove(col)

            genes.add(col)

        mutado.setGenes(genes)
        mutado.setRedundancias(self._calcularRedundancias(mutado.getGenes()))
        self._eliminarRedundancias(mutado)
        mutado.avaliarQualidade(self.pesoColunas)
        return mutado

    def __str__(self):
        # atributos ---------------------------------

        # numLinhas : int = -1
        # numColunas : int = -1
        # tamPop : int
        # dados: List[List[float]] = []               # linhas do documento de texto
        # self.pesoColunas : Dict[int, float] = {}           # {colunaID : peso}

        # self._linhasPorColuna : Dict[int, Set] = {}
        # self._colunasPorLinha : Dict[int, Set] = {}

        # self._populacaoAtual : List[Cromossomo] = []
        # self._populacaoRankeada : List[Cromossomo] = []

        # self._linhasDescobertas : Set[int] = set()

        bordaH : str = '-------------------------------------\n'

        nL : str = f'NUM LINHAS   : {self.numLinhas}\n'
        nC : str = f'NUM COLUNAS  : {self.numColunas}\n'

        pC : str = '' #self._stringPesoColunas()
        lPC : str = self._stringLinhasPorColuna()

        return bordaH + nL + nC + bordaH + pC + bordaH + lPC + bordaH

    def _stringPesoColunas(self) -> str:
        p = self.getPesoColunas()
        pC : str = 'Peso Colunas\n'
        for i in p:
            key = str(i)
            value = str(p[i])
            s = f'> {key} : {value}\n'
            pC = pC + s

        return pC

    def _stringLinhasPorColuna(self) -> str:
        l = self.getLinhasPorColunas()
        lPC : str = 'Linhas Por Colunas\n'
        for i in l:
            key = str(i)
            value = str(l[i])
            s = f'> {key} : {value}\n'
            lPC = lPC + s
        return lPC

    def exibirPopAtual(self):
        print('>> POPULAÇÃO ATUAL')
        for ind in self._populacaoAtual:
            print(ind)

        return

    def getNumLinhas(self) -> int:
        return self.numLinhas
    
    def getNumColunas(self) -> int:
        return self.numColunas
    
    def getTamPop(self) -> int:
        return self.tamPop

    def getDados(self) -> List[List[float]]:
        return self.dados
    
    def getPesoColunas(self) -> Dict[int, float]:
        return self.pesoColunas
    
    def getPesoDaColuna(self,coluna) -> float:
        return self.pesoColunas[coluna]
    
    def getLinhasPorColunas(self) -> Dict[int, Set[int]]:
        return self._linhasPorColuna
    
    def getLinhasDaColuna(self, coluna:int) -> Set[int]:
        return self._linhasPorColuna[coluna]

    def getColunasPorLinha(self) -> Dict[int, Set[int]]:
        return self._colunasPorLinha
    
    def getColunasDaLinha(self,linha:int) -> Set[int]:
        colunas = self._colunasPorLinha[linha]
        return colunas

    def getLinhasDescobertas(self) -> Set[int]:
        return self._linhasDescobertas
    

    def getCustoMenosApto(self) -> float:
        custo:float = self._populacaoAtual[0].getPeso()
        return custo
    
    def getCustoMaisApto(self) -> float:
        custo:float = self._populacaoAtual[-1].getPeso()
        return custo

    def setNumLinhas(self, num):
        self.numLinhas = num

    def setNumColunas(self, num):
        self.numColunas = num

    def setTamPop(self,tam:int):
        self.tamPop = tam
        return
    
    def setDados(self, dados):
        self.dados = dados
    
    def setPesoColunas(self, pesos):
        self.pesoColunas = pesos

    def setLinhasPorColuna(self, lpc):
        self._linhasPorColuna = lpc

    def setColunasPorLinhas(self, cpl):
        self._colunasPorLinha = cpl


    def setLinhasColunas(self):
        for j in range(1,self.numColunas+1):
           self._colunas.append(j)

        for i in range(1,self.numLinhas+1):
           self._linhas.append(i)
        return