import os
import json

json_file = 'decode_dict.json'

if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        decode_data = json.load(f)
else:
    decode_data = {}

sorted_json_file = 'sorted_data.json'
if os.path.exists(sorted_json_file):
    with open(sorted_json_file, 'r', encoding='utf-8') as f:
        sorted_data = json.load(f)
    
    for _, value in sorted_data.items():
        new_key = value.lower()[2:]
        if not new_key in decode_data:
            user_input = input(f"{new_key}: ")
            if user_input == 'qq':
                break
            else:
                decode_data[new_key] = user_input

with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(decode_data, f, ensure_ascii=False, indent=4)