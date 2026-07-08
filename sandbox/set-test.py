from typing import Set

def main():
    A : Set = {1,2,3,4,5}
    B : Set = {3,4,5,6,7}

    # operações
    # união      : A | B
    # interceção : A & B
    # diferença  : A - B
    # dif. simétrica : A ^ B
    # norma :  len(A)

    print(f'A | B = {A|B}')
    print(f'A & B = {A&B}')
    print(f'A - B = {A-B}')
    print(f'|A&B| = {len(A&B)}')

if __name__ == "__main__":
    main()
