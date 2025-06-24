import socket
import os
import threading
from backend.src.crypto.aes_256_gcm import CryptoManager
from backend.src.coding.b8t6 import LineCoding8B6T
from backend.src.plotting.plotting import Plotting

class Server:
    """
    Classe que encapsula a lógica do servidor de comunicação segura 8B6T
    """
    BUFFER_SIZE = 4096

    def __init__(self, host: str, port: int, secret_key: bytes, interface=None):
        """
        Inicializa o servidor com as configurações necessárias
        """
        self.host = host
        self.port = port
        self.secret_key = secret_key
        self.interface = interface
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.crypto_manager = CryptoManager(secret_key)
        self.line_coder = LineCoding8B6T()

        print("Servidor de comunicação segura 8B6T iniciado")
        print(f"Hash da chave secreta: {hash(secret_key)}")

    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """
        Método privado para lidar com a comunicação de um cliente
        """
        with client_socket:
            print(f"Conexão aceita de {address}")

            full_data = []
            while True:
                data_chunk = client_socket.recv(self.BUFFER_SIZE)
                if not data_chunk:
                    break
                full_data.append(data_chunk)

            sinal_recebido = b"".join(full_data).decode('utf-8')
            if not sinal_recebido:
                print("Cliente desconectou sem enviar dados")
                return

            print(f"Sinal 8B6T recebido: '{sinal_recebido}'")
            print(f"Sinal com {len(sinal_recebido)} símbolos")

            print("Decodificando o sinal 8B6T para obter a mensagem criptografada...")
            pacote_criptografado = self.line_coder.decode(sinal_recebido)
            mensagem_final = None

            if pacote_criptografado:
                print(f"Mensagem criptografada em hexadecimal: '{pacote_criptografado.hex()}'")
                print(f"Tamanho: {len(pacote_criptografado)} bytes. Descriptografando...")
                mensagem_final = self.crypto_manager.decrypt(pacote_criptografado)

                if mensagem_final:
                    print("Mensagem recuperada com sucesso:")
                    print(f"Hex: '{mensagem_final.hex()}'")
                    print(f"Texto: '{mensagem_final.decode('utf-8')}'")
                    client_socket.sendall(b"OK: mensagem recebida e decifrada com sucesso.")
                else:
                    print("Falha na verificação de integridade.")
                    client_socket.sendall(b"ERRO: falha na verificacao de seguranca.")
            else:
                print("Falha na decodificação do sinal.")
                client_socket.sendall(b"ERRO: falha na decodificacao do sinal.")

            # Atualiza interface se existir
            if self.interface:
                self.interface.update_results(
                    signal=sinal_recebido,
                    encrypted=pacote_criptografado.hex() if pacote_criptografado else "(erro na decodificação)",
                    decrypted=mensagem_final.decode('utf-8') if mensagem_final else "(falha na decriptação)"
                )

            print(f"Conexão com {address} encerrada")

    def start(self):
        """
        Inicia o servidor em modo de escuta (bloqueante)
        """
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Servidor escutando em {self.host}:{self.port}")
        print("Aguardando conexões...")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                self._handle_client(client_socket, address)
        except KeyboardInterrupt:
            print("Servidor encerrado pelo usuário.")
        finally:
            self.server_socket.close()
            print("Socket do servidor fechado.")

    def start_threaded(self):
        """
        Inicia o servidor em uma nova thread (modo interface gráfica)
        """
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()

# Execução direta via terminal
if __name__ == '__main__':
    HOST_ADDR = '0.0.0.0'
    PORT_NUM = 9999
    SECRET_KEY = os.urandom(32)

    print("Execute o cliente com esta chave secreta:")
    print(f"CHAVE HEX: {SECRET_KEY.hex()}")

    server = Server(host=HOST_ADDR, port=PORT_NUM, secret_key=SECRET_KEY)
    server.start()
