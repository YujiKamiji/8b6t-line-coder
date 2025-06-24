import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag

class CryptoManager:
    
    #classe para gerenciar a criptografia e descriptografia de dados usando o padraao AES-256-GCM.
    
    #constantes para os tamanhos.
    KEY_BYTES = 32  # Para AES-256
    IV_BYTES = 12   # Padrão recomendado para GCM
    TAG_BYTES = 16  # Padrão para GCM (128 bits)

    def __init__(self, key: bytes):
        """
        inicializa o gerenciador com uma chave secreta

        parametros:
            key (bytes): A chave secreta de 32 bytes (256 bits)
        """
        if len(key) != self.KEY_BYTES:
            raise ValueError(f"a chave para AES-256 deve ter exatamente {self.KEY_BYTES} bytes")
        self.key = key
        self.backend = default_backend()

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        criptografa os dados usando AES-GCM

        O metodo gera um IV (vetor de inicializacao) unico para cada criptografia e retorna um pacote de dados formatado da seguinte maneira:

        [IV (12 bytes)] + [Tag de Autenticacao (16 bytes)] + [Ciphertext (variavel)]

        parametros:
            plaintext (bytes): dados originais em seu formato legivel a serem criptografados

        retorno:
            bytes: o pacote de dados criptografados.
        """
        # 1: gerar um vetor de inicializacao (IV) novo e aleatorio para cada criptografia (na real eh pseudoaleatorio ne, mas o metodo os.urandom() 
        # entra na categoria de "numeros pseudorrandomicos criptograficamente seguros" (CSPRNG), ele faz uma chamada muito doida ao sistema operacional para obter bytes imprevisiveis)
        iv = os.urandom(self.IV_BYTES)

        # 2: criar o objeto de cifra AES no modo GCM
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # 3: criptografar os dados
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # 4: a tag de autenticacao eh gerada automaticamente pelo encryptor
        auth_tag = encryptor.tag

        # 5: montar o pacote final para envio, a ordem eh crucial e deve ser
        # a mesma na descriptografia
        return iv + auth_tag + ciphertext

    def decrypt(self, encrypted_package: bytes) -> bytes | None:
        """
        descriptografa um pacote de dados AES-GCM

        espera um pacote no formato:
        [IV (12 bytes)] + [Tag de Autenticacao (16 bytes)] + [Ciphertext (variavel)]

        verifica a tag de autenticacao, se a verificacao falhar (indicando
        dados corrompidos ou chave incorreta), retorna none

        parametros:
            encrypted_package (bytes): o pacote de dados criptografados

        retorno:
            bytes | None: Os dados originais em caso de sucesso, ou none se a
                          autenticacao falhar
        """
        # verifica se o pacote tem o tamanho minimo para conter o iv e a tag
        if len(encrypted_package) < self.IV_BYTES + self.TAG_BYTES:
            print("Erro: Pacote criptografado invalido ou muito curto")
            return None

        try:
            # 1: desmontar o pacote na mesma ordem em que foi montado
            iv = encrypted_package[:self.IV_BYTES]
            auth_tag = encrypted_package[self.IV_BYTES : self.IV_BYTES + self.TAG_BYTES]
            ciphertext = encrypted_package[self.IV_BYTES + self.TAG_BYTES:]

            # 2: criar o objeto de cifra, fornecendo o IV e a TAG para verificaçao
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, auth_tag), backend=self.backend)
            decryptor = cipher.decryptor()

            # 3: descriptografar, a biblioteca vai automaticamente verificar a tag
            # se a tag for invalida, uma excecao 'InvalidTag' sera gerada aqui.
            decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            
            return decrypted_bytes
        
        except InvalidTag:
            print("Falha na descriptografia: A TAG DE AUTENTICACAO É INVALIDA")
            print("Isso significa que a chave está incorreta ou os dados foram corrompidos")
            return None
        except Exception as e:
            print(f"Ocorreu um erro inesperado na descriptografia: {e}")
            return None