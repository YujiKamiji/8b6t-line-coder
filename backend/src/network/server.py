import socket
import os
from src.crypto.aes_256_gcm import CryptoManager
from src.coding.b8t6 import LineCoding8B6T
from src.plotting.plotting import Plotting

class Server:
    """
    classe que encapsula a logica do servidor de comunicacao
    """
    BUFFER_SIZE = 4096

    def __init__(self, host: str, port: int, secret_key: bytes):
        """
        inicializa o servidor com as configuracoes necessarias
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.crypto_manager = CryptoManager(secret_key)
        self.line_coder = LineCoding8B6T()
        print("servidor de comunicacao segura 8b6t iniciado")
        print(f"hash da chave secreta: {hash(secret_key)}")

    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """
        metodo privado para lidar com a comunicacao de um cliente
        """
        with client_socket:
            print(f"conexao aceita de {address}")
            
            full_data = []
            while True:
                data_chunk = client_socket.recv(self.BUFFER_SIZE)
                if not data_chunk:
                    break
                full_data.append(data_chunk)
            
            sinal_recebido = b"".join(full_data).decode('utf-8')
            if not sinal_recebido:
                print("cliente desconectou sem enviar dados")
                return

            print(f"sinal 8b6t recebido: '{sinal_recebido}'")
            print(f"sinal 8b6t recebido com ({len(sinal_recebido)} simbolos)")
            #Plotting.plot_8b6t(sinal_recebido, save_path="grafico_8b6t_recebimento.png")

            print("decodificando o sinal 8b6t para obter a mensagem criptografada")
            pacote_criptografado = self.line_coder.decode(sinal_recebido)

            if pacote_criptografado:
                print(f"mensagem criptografada no formato hexadecimal: '{pacote_criptografado.hex()}'")
                print(f"tamanho da mensagem criptografada: ({len(pacote_criptografado)} bytes), descriptografando")
                mensagem_final = self.crypto_manager.decrypt(pacote_criptografado)
                
                if mensagem_final:
                    print("mensagem recuperada e verificada:")
                    print(f"conteudo em hexadecimal: '{mensagem_final.hex()}' ")
                    print(f"conteudo original: '{mensagem_final.decode('utf-8')}'")
                    client_socket.sendall(b"OK: mensagem recebida e decifrada com sucesso.")
                else:
                    print("falha na descriptografia")
                    client_socket.sendall(b"ERRO: falha na verificacao de seguranca.")
            else:
                print("falha na decodificacao do sinal")
                client_socket.sendall(b"ERRO: falha na decodificacao do sinal.")
        
        print(f"conexao com {address} encerrada")

    def start(self):
        """
        inicia o servidor para escutar por conexoes
        """
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"servidor escutando em {self.host}:{self.port}")
        print("aguardando conexoes")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                self._handle_client(client_socket, address)
        except KeyboardInterrupt:
            print("servidor encerrado pelo usuario")
        finally:
            self.server_socket.close()
            print("socket do servidor fechado")

if __name__ == '__main__':
    HOST_ADDR = '0.0.0.0'
    PORT_NUM = 9999
    SECRET_KEY = os.urandom(32)
    
    print("Execute o cliente com esta chave secreta:")
    print(f"CHAVE HEX: {SECRET_KEY.hex()}")
    
    server = Server(host=HOST_ADDR, port=PORT_NUM, secret_key=SECRET_KEY)
    server.start()