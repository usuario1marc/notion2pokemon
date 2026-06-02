import pandas as pd
import json
import os

export_filepath = r"C:\Users\madro\OneDrive\Escritorio\POKEMON MALLORCA\notion_exports\2026_06_02"
output_filepath = r"C:\Users\madro\OneDrive\Escritorio\POKEMON MALLORCA\notion parser\output"

# Helper function to safely parse integers
def parse_int(val):
    if pd.isna(val): return 0
    try: return int(float(val))
    except: return 0

# Helper function to parse lists into a list of ints
def parse_props(val):
    if pd.isna(val): return []
    if isinstance(val, str):
        return [int(x.strip()) for x in val.split(',') if x.strip().isdigit()]
    return []

def parse_moves(root, output_filepath):
    file = os.path.join(root, "Moviments 33c77b2f7abc802ca2d2c4d6db4becf4_all.csv")
    df = pd.read_csv(file)
    
    # Keep only those included in the game
    df = df[df['inclòs al joc'] == 'Yes'].copy()

    # Mappings for categorical columns
    categoria_map = {
        'Físic': 1,
        'Especial': 2,
        'Estat': 3
    }
    objectiu_map = {
        'Usuari': 1,
        'Elegit': 2,
        'Oponent aleatori': 3,
        'Oponents adjacents': 4,
        'Pokémon adjacents': 5,
        'Aliat elegit': 6,
        'Usuari o aliat elegit': 7,
        'Tots els aliats': 8,
        'Bàndol aliat': 9,
        'Bàndol contrari': 10,
        'Tots': 11
    }

    moves_dict = {}
    moves_list_by_id = {}
    max_id = 0

    for _, row in df.iterrows():
        # Get ID and update max_id to build the Godot array size later
        m_id = parse_int(row['id'])
        if m_id > max_id:
            max_id = m_id
        
        catala = str(row['català'])
        tipus = parse_int(row['idx tipus'])
        
        cat_str = str(row['categoria']) if pd.notna(row['categoria']) else ''
        categoria = categoria_map.get(cat_str, 0)
        
        obj_str = str(row['objectiu']) if pd.notna(row['objectiu']) else ''
        objectiu = objectiu_map.get(obj_str, 0)
        
        potencia = parse_int(row['potència'])
        precisio = parse_int(row['precisió'])
        pp = parse_int(row['pp base'])
        prioritat = parse_int(row['prioritat'])
        probabilitat = parse_int(row['probabilitat'])
        efecte = parse_int(row['idx efecte'])
        propietats = parse_props(row['idx propietat'])
        
        # 1. Structure for the Dictionary JSON
        moves_dict[catala] = {
            "id": m_id,
            "tipus": tipus,
            "categoria": categoria,
            "objectiu": objectiu,
            "potencia": potencia,
            "precisio": precisio,
            "pp": pp,
            "prioritat": prioritat,
            "probabilitat_efecte": probabilitat,
            "efecte": efecte,
            "propietats": propietats # Represented as a standard list [0, 1, 2, 4] for JSON standard
        }
        
        # 2. Structure for Godot
        moves_list_by_id[m_id] = [
            catala, tipus, categoria, objectiu, potencia, precisio, pp, 
            prioritat, probabilitat, efecte, propietats
        ]

    # Save format 1: Tabbed JSON File 
    dict_path = os.path.join(output_filepath, 'moves_dict.json')
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(moves_dict, f, ensure_ascii=False, indent=4)

    # Save format 2: Godot Array where index == ID
    # We create an array of size (max_id + 1) filled with empty arrays `[]`
    godot_array = [[] for _ in range(max_id + 1)]
    for move_id, move_data in moves_list_by_id.items():
        godot_array[move_id] = move_data

    godot_path = os.path.join(output_filepath, 'moves_godot.json')
    with open(godot_path, 'w', encoding='utf-8') as f:
        json.dump(godot_array, f, ensure_ascii=False, indent=4)

    print(f"Exported successfully to:\n{dict_path}\n{godot_path}")

# Run the parser
parse_moves(export_filepath, output_filepath)