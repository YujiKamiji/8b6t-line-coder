import json
from pathlib import Path

class LineCoding8B6T:
    def __init__(self):
        self.mapping_table = {}             #tabela de mapeamento para codificação
        self.reverse_mapping_table = {}     #tabela de mapeamento reversa para decodificação rapida
        self.dc_balance = 0                 #contador de balanceamento DC
        self._initialize_tables()           #chama o método para inicializar as tabelas

    def _initialize_tables(self):           #preencher as tabelas de mapeamento
        json_path = Path(__file__).parent / 'b8t6_table.json'
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data_from_json = json.load(file)

        self.mapping_table = {int(key, 16): value for key, value in data_from_json.items()} # converte as chaves hexadecimais para inteiros

        for byte_val, value in self.mapping_table.items():
            self.reverse_mapping_table[value['code']] = byte_val

    def encode(self, data_bytes: bytes) -> str: #codifica uma sequência de bytes para uma string ternária 8b6t
        encoded_symbols = []
        
        # self.dc_balance deve ser resetado ou mantido, dependendo do escopo da conexão.
        # para uma transmissão única, resetar a cada chamada é uma opção.
        self.dc_balance = 0

        for byte in data_bytes:
            entry = self.mapping_table.get(byte)
            if not entry:
                raise ValueError(f"Byte {hex(byte)} não encontrado na tabela de mapeamento.")

            code_to_send = entry['code']
            weight = entry['weight']

            #a logica de balanceamento de DC
            if weight == 1 and self.dc_balance > 0:
                #inverte o código para balancear a linha
                code_to_send = code_to_send.replace('+', 't').replace('-', '+').replace('t', '-')
                self.dc_balance -= 1  #o bloco invertido tem peso -1
            else:
                self.dc_balance += weight
            
            encoded_symbols.append(code_to_send)
        
        return "".join(encoded_symbols)

    def decode(self, ternary_string: str) -> bytes: #decodifica uma string ternária 8B6T para a sequência de bytes original
        if len(ternary_string) % 6 != 0:
            raise ValueError("A string ternária de entrada tem um tamanho inválido.")

        decoded_bytes = []
        
        #processa a string em blocos de 6 símbolos
        for i in range(0, len(ternary_string), 6):
            block = ternary_string[i:i+6]
            
            #verifica o peso do bloco para saber se foi invertido
            weight = block.count('+') - block.count('-')
            
            if weight == -1:
                #eh um bloco invertido, desfaz a inversao para encontrar na tabela
                block = block.replace('+', 't').replace('-', '+').replace('t', '-')
            
            #busca o byte na tabela inversa
            original_byte = self.reverse_mapping_table.get(block)
            if original_byte is None:
                raise ValueError(f"Bloco ternário '{block}' não reconhecido.")
                
            decoded_bytes.append(original_byte)

        return bytes(decoded_bytes)