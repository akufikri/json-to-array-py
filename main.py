import os
import json

input_folder = 'input'
output_folder = 'output'

def json_to_laravel_array(data, indent=0):
    def convert(value, indent):
        def try_decode_json(value):
            try:
                decoded = json.loads(value)
                if isinstance(decoded, (dict, list)):
                    return decoded
            except (json.JSONDecodeError, TypeError):
                pass
            return value

        value = try_decode_json(value)

        if isinstance(value, dict):
            items = [f"{' ' * (indent + 4)}'{k}' => {convert(v, indent + 4)}" for k, v in value.items()]
            return "[\n" + ",\n".join(items) + f"\n{' ' * indent}]"
        elif isinstance(value, list):
            items = [f"{' ' * (indent + 4)}{convert(v, indent + 4)}" for v in value]
            return "[\n" + ",\n".join(items) + f"\n{' ' * indent}]"
        elif isinstance(value, str):
            return f"'{value.replace('\'', '\\\'')}'"
        elif value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        else:
            return str(value)

    return '<?php\n\nreturn ' + convert(data, indent) + ';\n'

def decode_if_encoded(data):
    if isinstance(data, (list, dict)):
        return data
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return data

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        input_path = os.path.join(input_folder, filename)
        with open(input_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            data = decode_if_encoded(data)
            laravel_array = json_to_laravel_array(data)
            output_filename = os.path.splitext(filename)[0] + '.php'
            output_path = os.path.join(output_folder, output_filename)
            with open(output_path, 'w', encoding='utf-8') as php_file:
                php_file.write(laravel_array)

print("Konversi selesai. File PHP disimpan di folder 'output'.")
