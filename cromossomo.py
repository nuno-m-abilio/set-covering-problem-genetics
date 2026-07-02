from typing import Set,List

class Cromossomo():
    def __init__(self,genes : Set[int] | None = None):
        self._peso : float = 0
        self._genes : Set[int]

        self._redundancias : List[int]

        self._probabilidade : float
        if genes is not None:
            self._genes : Set[int] = genes

    # ----- API -----
    # eliminarRedundancias()
    # avaliarQualidade()

    def avaliarQualidade(self,pesos):
        for gene in self._genes:
            self._peso += pesos[gene]
        return

    def removeGene(self,gene:int,linhas:Set[int]):
        """
        Remove *gene* da lista de genes e atualiza os valores de redundância das *linhas*
        """
        self._genes.remove(gene)

        for linha in linhas:
            self._redundancias[linha] -= 1
        return

    def ehRedundante(self,linhas:Set[int]) -> bool:
        """
        Retorna True se todas linhas sao redundantes e False caso contrario
        """
        ehRedundante : bool = True
        for linha in linhas:
            if self._redundancias[linha] < 2: 
                ehRedundante = False
        return ehRedundante
    
    def getRedundancias(self) -> List[int]:
        return self._redundancias

    def getPeso(self) -> float:
        return self._peso
    
    def getGenes(self) -> Set[int]:
        return self._genes
    
    def getProbabilidade(self) -> float:
        return self._probabilidade

    def setGenes(self,genes:Set[int],):
        self._genes = genes

        return
    
    def setRedundancias(self,redundancias:list[int]):
        self._redundancias = redundancias
        return

    def setProbabilidade(self,prob:float):
        self._probabilidade = prob
        return    

    def __str__(self) -> str:
        a = f'---------------\n   INDIVIDUO   \n---------------\n| PESO : {self._peso} \n| GENES : {self._genes}'
        return a