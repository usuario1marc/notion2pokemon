import pandas as pd
import json
import os
import re

export_filepath = r"C:\Users\madro\OneDrive\Escritorio\POKEMON MALLORCA\notion_exports\2026_06_02"
output_filepath = r"C:\Users\madro\OneDrive\Escritorio\POKEMON MALLORCA\notion2pokemon\output"

def parse_int(val):
    if pd.isna(val): return 0
    try: return int(float(val))
    except: return 0

def parse_list(val):
    if pd.isna(val): return []
    if isinstance(val, str):
        return sorted([int(x.strip()) for x in val.split(',') if x.strip().isdigit()])
    return []

def parse_moves(root, output_filepath):
    file = os.path.join(root, "Moviments 33c77b2f7abc802ca2d2c4d6db4becf4_all.csv")
    df = pd.read_csv(file)
    
    # Guarda només els que estiguin al joc
    df = df[df['inclòs al joc'] == 'Yes'].copy()

    categoria_map = {
        'Físic': 0,
        'Especial': 1,
        'Estat': 2
    }
    objectiu_map = {
        'Usuari': 0,
        'Elegit': 1,
        'Oponent aleatori': 2,
        'Oponents adjacents': 3,
        'Pokémon adjacents': 4,
        'Aliat elegit': 5,
        'Usuari o aliat elegit': 6,
        'Tots els aliats': 7,
        'Bàndol aliat': 8,
        'Bàndol contrari': 9,
        'Tots': 10
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
        categoria = categoria_map.get(cat_str, 3)
        
        obj_str = str(row['objectiu']) if pd.notna(row['objectiu']) else ''
        objectiu = objectiu_map.get(obj_str, 11)
        
        potencia = parse_int(row['potència'])
        precisio = parse_int(row['precisió'])
        pp = parse_int(row['pp base'])
        prioritat = parse_int(row['prioritat'])
        probabilitat = parse_int(row['probabilitat'])
        efecte = parse_int(row['idx efecte'])
        propietats = parse_list(row['idx propietat'])
        
        # 1. Estructura del JSON interpretable
        moves_dict[catala] = {
            "id": m_id,
            "tipus": tipus,
            "categoria": categoria,
            "potencia": potencia,
            "precisio": precisio,
            "pp": pp,
            "prioritat": prioritat,
            "propietats": propietats,
            "probabilitat_efecte": probabilitat,
            "efecte": efecte,
            "objectiu": objectiu
        }
        
        # 2. Estructura per Godot
        moves_list_by_id[m_id] = [
            catala, tipus, categoria, potencia, precisio, pp, prioritat, propietats, probabilitat, efecte, objectiu
        ]

    # 1.
    dict_path = os.path.join(output_filepath, 'moves_dict.json')
    moves_dict_sorted = {k: moves_dict[k] for k in sorted(moves_dict.keys())}
    json_string = json.dumps(moves_dict_sorted, ensure_ascii=False, indent=4)
    json_string_clean = re.sub(r'\[\s+([^\[\]]*?)\s+\]', lambda m: '[' + re.sub(r'\s+', ' ', m.group(1)) + ']', json_string)
    dict_path = os.path.join(output_filepath, 'moves_dict.json')
    with open(dict_path, 'w', encoding='utf-8') as f:
        f.write(json_string_clean)

    # 2.
    godot_array = [[] for _ in range(max_id + 1)]
    for move_id, move_data in moves_list_by_id.items():
        godot_array[move_id] = move_data
    godot_path = os.path.join(output_filepath, 'moves_godot.json')
    with open(godot_path, 'w', encoding='utf-8') as f:
        json.dump(godot_array, f, ensure_ascii=False)

    print(f"Exported successfully to:\n{dict_path}\n{godot_path}")

# Run the parser
parse_moves(export_filepath, output_filepath)