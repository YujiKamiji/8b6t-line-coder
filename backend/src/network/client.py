import socket
import os
from src.crypto.aes_256_gcm import CryptoManager
from src.coding.b8t6 import LineCoding8B6T
from src.plotting.plotting import Plotting

class Client:
    """
    classe que encapsula a logica para o cliente da comunicacao
    """
    BUFFER_SIZE = 4096

    def __init__(self, host: str, port: int, secret_key: bytes):
        """
        inicializa o cliente com os detalhes do servidor e a chave secreta
        """
        self.host = host
        self.port = port
        self.crypto_manager = CryptoManager(secret_key)
        self.line_coder = LineCoding8B6T()
        print("cliente de comunicacao segura 8b6t iniciado")
        print(f"conectando em {self.host}:{self.port}")

    def send_message(self, message: str):
        """
        processa uma mensagem (criptografa, codifica) e envia ao servidor
        """
        print(f"preparando a mensagem: '{message}'")
        
        message_bytes = message.encode('utf-8')
        print("criptografando a mensagem")

        pacote_criptografado = self.crypto_manager.encrypt(message_bytes)
        print(f"mensagem criptografada no formato hexadecimal: '{pacote_criptografado.hex()}'")
        print(f"tamanho da mensagem criptografada: ({len(pacote_criptografado)} bytes)")

        print("codificando os dados criptografados em formato 8b6t")
        sinal_para_enviar = self.line_coder.encode(pacote_criptografado)
        print(f"sinal 8b6t: '{sinal_para_enviar}'")
        print(f"sinal 8b6t gerado com ({len(sinal_para_enviar)} simbolos)")
        #Plotting.plot_8b6t(sinal_para_enviar, save_path="grafico_8b6t_envio.png")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                print(f"conectando ao servidor em {self.host}:{self.port}")
                client_socket.connect((self.host, self.port))
                print("conexao estabelecida")

                client_socket.sendall(sinal_para_enviar.encode('utf-8'))
                client_socket.shutdown(socket.SHUT_WR)

                print("sinal enviado")
                print("aguardando resposta do servidor")
                response = client_socket.recv(self.BUFFER_SIZE)
                print(f"resposta recebida: '{response.decode('utf-8')}'")
        
        except ConnectionRefusedError:
            print("erro: conexao recusada. verifique se o servidor esta rodando e o endereco/porta estao corretos")
        except socket.gaierror:
            print(f"erro: endereco do host '{self.host}' nao encontrado")
        except Exception as e:
            print(f"erro inesperado na rede: {e}")

if __name__ == '__main__':
    server_ip = input("digite o endereco ip do servidor: ")
    server_port = 9999
    key_hex = input("cole a chave secreta (em hexadecimal) gerada pelo servidor: ")

    try:
        secret_key_from_server = bytes.fromhex(key_hex)
    except ValueError:
        print("erro: formato da chave hexadecimal invalido")
        exit(1)

    try:
        client = Client(host=server_ip, port=server_port, secret_key=secret_key_from_server)

        while True:
            message_to_send = input("digite a mensagem (ou 'sair' para encerrar): ")
            if message_to_send.lower() == 'sair':
                break
            client.send_message(message_to_send)

    except ValueError as e:
        print(f"erro de valor durante o envio: {e}")
    except Exception as e:
        print(f"erro inesperado: {e}")
    
    print("cliente encerrado")
