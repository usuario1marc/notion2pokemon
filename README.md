# notion2pokemon

## Processament de moviments
L'estructura de dades per als moviments és una llista de llistes (array d'arrays).

    all_moves_array = [ move_array_ID0 = [...], move_array_ID1 = [...], ... ]

L'ID d'un moviment correspon directament al seu índex dins de `all_moves_array`.
Cada `move_array` conté els següents elements en aquest ordre:

    move_array_IDX = [
        #0  nom en català (string)
        #1  tipus (int)
        #2  categoria (int)
        #3  potencia (int)
        #4  precisio (int)
        #5  pp (int)
        #6  prioritat (int)
        #7  propietats = [...] (array d'int)
        #8  probabilitat_efecte (int)
        #9  efecte (int)
        #10 objectiu (int)
    ]

Tingues en compte que tant la categoria com l'objectiu s'han convertit a valors enters mitjançant la següent equivalència:

    Categoria
        'Físic': 0
        'Especial': 1
        'Estat': 2
        (altre): 3

    Objectiu
        'Usuari': 0
        'Elegit': 1
        'Oponent aleatori': 2
        'Oponents adjacents': 3
        'Pokémon adjacents': 4
        'Aliat elegit': 5
        'Usuari o aliat elegit': 6
        'Tots els aliats': 7
        'Bàndol aliat': 8
        'Bàndol contrari': 9
        'Tots': 10
        (altre): 11

També es genera un fitxer JSON addicional que és més fàcil de llegir per a humans, el qual inclou etiquetes descriptives textuals.