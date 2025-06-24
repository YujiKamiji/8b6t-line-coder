import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from backend.src.network.client import Client 
from backend.src.plotting.plotting import Plotting

class ClientScreen(tk.Frame):
    def __init__(self, master=None, on_back=None):
        super().__init__(master)
        self.master = master
        self.on_back = on_back

        # Entrada de IP
        self.label_ip = ttk.Label(self, text="Endereço IP do servidor:")
        self.label_ip.pack(pady=(10, 0))
        self.entry_ip = ttk.Entry(self, width=40)
        self.entry_ip.pack(pady=5)

        # Entrada de Porta
        self.label_porta = ttk.Label(self, text="Porta do servidor:")
        self.label_porta.pack(pady=(10, 0))
        self.entry_porta = ttk.Entry(self, width=40)
        self.entry_porta.pack(pady=5)

        # Entrada da chave
        self.label_chave = ttk.Label(self, text="Chave secreta (hexadecimal):")
        self.label_chave.pack(pady=(10, 0))
        self.entry_chave = ttk.Entry(self, width=40)
        self.entry_chave.pack(pady=5)

        # Entrada da mensagem
        self.label_mensagem = ttk.Label(self, text="Mensagem a ser enviada:")
        self.label_mensagem.pack(pady=(10, 0))
        self.entry_mensagem = ttk.Entry(self, width=40)
        self.entry_mensagem.pack(pady=5)

        # Botão para enviar
        self.botao_enviar = ttk.Button(self, text="Enviar Mensagem", command=self.enviar_mensagem)
        self.botao_enviar.pack(pady=20)

        # Botão de voltar
        if self.on_back:
            self.botao_voltar = ttk.Button(self, text="Voltar", command=self.on_back)
            self.botao_voltar.pack(pady=(0, 20))

        # Campos de resultado
        self.resultado_frame = ttk.Frame(self)
        self.label_pacote = ttk.Label(self.resultado_frame, text="Mensagem criptografada (hex):")
        self.valor_pacote = tk.Text(self.resultado_frame, height=2, width=60, wrap='word')

        self.label_codificado = ttk.Label(self.resultado_frame, text="Sinal enviado (8B6T):")
        self.valor_codificado = tk.Text(self.resultado_frame, height=4, width=60, wrap='word')

    def enviar_mensagem(self):
        ip = self.entry_ip.get()

        try:
            porta = int(self.entry_porta.get())
        except ValueError:
            print("Porta inválida")
            return

        chave = self.entry_chave.get()
        mensagem = self.entry_mensagem.get()

        if not mensagem.strip():
            print("Mensagem vazia.")
            return

        # lógica de criptografia e codificação
        try:
            secret_key_from_server = bytes.fromhex(chave)
        except ValueError:
            print("erro: formato da chave hexadecimal inválido")
            return

        try:
            client = Client(host=ip, port=porta, secret_key=secret_key_from_server)
            pacote_hex, sinal_8b6t = client.send_message(mensagem)
            
        except Exception as e:
            print(f"erro ao enviar mensagem: {e}")
            return

        # Mostrar resultados na interface
        self.resultado_frame.pack(pady=10, fill='x')

        self.label_pacote.pack(anchor='w')
        self.valor_pacote.pack()
        self.valor_pacote.delete("1.0", tk.END)
        self.valor_pacote.insert(tk.END, pacote_hex)

        self.label_codificado.pack(anchor='w', pady=(10, 0))
        self.valor_codificado.pack()
        self.valor_codificado.delete("1.0", tk.END)
        self.valor_codificado.insert(tk.END, sinal_8b6t)

        plt.close('all')
        Plotting.plot_8b6t(sinal_8b6t)
