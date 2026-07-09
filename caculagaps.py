referência = {
    "test01" : 557.44,
    "test02" : 537.89,
    "test03" : 517.58,
    "test04" : 1162.8,
    "test05" : 1020.12,
    "wren01" : 7856.0,
    "wren02" : 13908.0,
    "wren03" : 13780.0,
    "wren04" : 58161.0
}

melhores = {
    "test01" : 696.06,
    "test02" : 701.29,
    "test03" : 681.69,
    "test04" : 1489.97,
    "test05" : 1284.53,
    "wren01" : 8941.00,
    "wren02" : 17951.00,
    "wren03" : 18150.00,
    "wren04" : 73133.00 
}

gaps = {}

def main():
    for key in referência:
        gap = (melhores[key] - referência[key]) / referência[key]
        gaps.update({key:gap})

    for key, value in gaps.items():
        print(f'({key} : {value})')

if __name__ == "__main__":
    main()