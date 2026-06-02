# notion2pokemon

## Processament de moviments
L'estructura de dades per als moviments és una llista de llistes (array d'arrays).

    all_moves_array = [ move_array_1=[], move_array_2=[], ... ]

L'ID d'un moviment correspon directament al seu índex dins de `all_moves_array`.
Cada `move_array` conté els següents elements en aquest ordre:

    move_array_ID = [
        #0  nom en català (string),
        #1  tipus (int),
        #2  categoria (int),
        #3  objectiu (int),
        #4  potencia (int),
        #5  precisio (int),
        #6  pp (int),
        #7  prioritat (int),
        #8  probabilitat_efecte (int),
        #9  efecte (int),
        #10 propietats = [...] (array de int)
    ]

Tingues en compte que tant la categoria com l'objectiu s'han convertit a valors enters mitjançant la següent equivalència:

    Categoria
        'Físic': 1
        'Especial': 2
        'Estat': 3

    Objectiu
        'Usuari': 1
        'Elegit': 2
        'Oponent aleatori': 3
        'Oponents adjacents': 4
        'Pokémon adjacents': 5
        'Aliat elegit': 6
        'Usuari o aliat elegit': 7
        'Tots els aliats': 8
        'Bàndol aliat': 9
        'Bàndol contrari': 10
        'Tots': 11

També es genera un fitxer JSON addicional que és més fàcil de llegir per a humans, el qual inclou etiquetes descriptives textuals.