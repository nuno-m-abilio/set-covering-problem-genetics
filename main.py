import utils

from sys import argv

def main(caminho:str):
    dados = utils.LerDados(caminho)

    for d in dados:
        print(d)


if __name__ == "__main__":
    if len(argv) == 1:
        print("ERROR : Missing argument file path")
    else:
        main(argv[1])
