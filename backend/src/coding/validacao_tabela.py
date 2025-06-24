import json
from pathlib import Path

json_path = Path(__file__).parent / "b8t6_table.json"

with open(json_path, encoding="utf-8") as f:
    table = json.load(f)

faltando = []

for i in range(256):
    hex_key = f"0x{i:02X}"
    if hex_key not in table:
        faltando.append(hex_key)

print(f"{len(faltando)} entradas faltando:")
print(faltando)
