import os
import json

def save_file(json_data) -> None:
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'data.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)
        
def read_file():
    try:
        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'data.json')
        f = open(file_path)
        json_data = json.load(f)
        return json_data
    except FileNotFoundError: 
        print("File not found, returning empty")
        return {}