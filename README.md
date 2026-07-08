# Set Covering Problem - Algoritmo Genético

Este projeto implementa uma solução baseada em Algoritmos Genéticos para resolver o **Problema de Cobertura de Conjuntos (Set Covering Problem)**. O sistema permite configurar e rodar baterias de testes automatizados variando diversos parâmetros do algoritmo.

## Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado na sua máquina. Não são necessárias bibliotecas externas adicionais, pois o projeto utiliza apenas pacotes nativos da linguagem (`json`, `typing`, `functools`, etc.).

### 2. Configuração dos Casos de Teste (`tests-config.json`)
Antes de rodar o projeto, você deve configurar o arquivo `tests-config.json` na raiz do diretório. Esse arquivo define quais instâncias serão testadas e os parâmetros do algoritmo genético que serão combinados.

Exemplo de estrutura do `tests-config.json`:
```json
{
    "diretorio": "tests/",
    "testes": ["test01.dat", "test02.dat"],
    "execucoes": 10,
    "parametros": {
        "tamanho-populacao": [50, 100],
        "taxa-mutacao-minima": [0.01, 0.05],
        "numero-iteracoes": [100, 500]
    }
}

```

* **`diretorio`**: Caminho da pasta onde os arquivos de dados dos problemas (`.dat`) estão armazenados.
* **`testes`**: Lista com os nomes dos arquivos de teste que deseja executar.
* **`execucoes`**: Quantidade de vezes que cada combinação de parâmetros será executada (para fins de análise estatística/média).
* **`parametros`**: Listas de parâmetros (`tamanho-populacao`, `taxa-mutacao-minima`, `numero-iteracoes`) que o algoritmo irá combinar e testar exaustivamente.

### 3. Executando os Testes

Para iniciar a bateria de execuções configurada, basta rodar o arquivo principal (`main.py`):

```bash
python main.py

```

## Resultados dos Testes

O script criará (ou atualizará) arquivos de resultados no formato JSON dentro da pasta `tests-results/` (certifique-se de que esta pasta existe no seu diretório antes de rodar).

Cada arquivo conterá um histórico detalhado das baterias executadas para aquele arquivo de teste, incluindo:

* Parâmetros utilizados (população, mutação, iterações).
* O custo da melhor solução encontrada em cada execução (`melhores-custos`).
* O tempo de execução de cada rodada (`tempos-execucao`).
* O tempo médio final daquela configuração (`tempo-exec-medio`).

```