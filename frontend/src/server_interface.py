import tkinter as tk
from tkinter import ttk
import os
import matplotlib.pyplot as plt
from backend.src.network.server import Server
from backend.src.plotting.plotting import Plotting

class ServerScreen(tk.Frame):
    def __init__(self, master=None, on_back=None):
        super().__init__(master)
        self.master = master
        self.on_back = on_back

        self.host = "0.0.0.0"
        self.port = 9999
        self.secret_key = os.urandom(32)

        self.create_widgets()
        self.setup_server()

    def create_widgets(self):
        tk.Label(self, text="Servidor - Receber Mensagem", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # IP
        tk.Label(self, text="IP em escuta:").grid(row=1, column=0, sticky="e")
        self.ip_entry = tk.Entry(self, width=50, state='readonly')
        self.ip_entry.grid(row=1, column=1, sticky="w")
        self.ip_entry.config(state='normal')
        self.ip_entry.insert(0, self.host)
        self.ip_entry.config(state='readonly')

        # Porta
        tk.Label(self, text="Porta:").grid(row=2, column=0, sticky="e")
        self.port_entry = tk.Entry(self, width=50, state='readonly')
        self.port_entry.grid(row=2, column=1, sticky="w")
        self.port_entry.config(state='normal')
        self.port_entry.insert(0, str(self.port))
        self.port_entry.config(state='readonly')

        # Chave
        tk.Label(self, text="Chave gerada:").grid(row=3, column=0, sticky="e")
        self.key_entry = tk.Entry(self, width=50, state='readonly')
        self.key_entry.grid(row=3, column=1, sticky="w")
        self.key_entry.config(state='normal')
        self.key_entry.insert(0, self.secret_key.hex())
        self.key_entry.config(state='readonly')

        # Hash
        tk.Label(self, text="Hash da chave:").grid(row=4, column=0, sticky="e")
        self.hash_entry = tk.Entry(self, width=50, state='readonly')
        self.hash_entry.grid(row=4, column=1, sticky="w")
        self.hash_entry.config(state='normal')
        self.hash_entry.insert(0, str(hash(self.secret_key)))
        self.hash_entry.config(state='readonly')

        # Separador
        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # Sinal 8B6T
        tk.Label(self, text="Sinal 8B6T recebido:").grid(row=6, column=0, sticky="ne")
        self.signal_text = tk.Text(self, height=3, width=60, wrap="word", state='disabled')
        self.signal_text.grid(row=6, column=1, sticky="w")

        # Criptografada
        tk.Label(self, text="Mensagem criptografada:").grid(row=7, column=0, sticky="ne")
        self.encrypted_text = tk.Text(self, height=3, width=60, wrap="word", state='disabled')
        self.encrypted_text.grid(row=7, column=1, sticky="w")

        # Decriptada
        tk.Label(self, text="Mensagem decriptada:").grid(row=8, column=0, sticky="ne")
        self.decrypted_text = tk.Text(self, height=3, width=60, wrap="word", state='disabled')
        self.decrypted_text.grid(row=8, column=1, sticky="w")

        if self.on_back:
            self.back_button = tk.Button(self, text="Voltar", command=self.on_back)
            self.back_button.grid(row=9, column=0, columnspan=2, pady=20)

    def setup_server(self):
        self.server = Server(
            host=self.host,
            port=self.port,
            secret_key=self.secret_key,
            interface=self
        )
        self.server.start_threaded()

    def update_results(self, signal, encrypted, decrypted):
        self._set_text(self.signal_text, signal)
        self._set_text(self.encrypted_text, encrypted)
        self._set_text(self.decrypted_text, decrypted)
        plt.close('all')
        Plotting.plot_8b6t(signal)

    def update_info(self, ip, port, key, hash_):
        self._set_entry(self.ip_entry, ip)
        self._set_entry(self.port_entry, str(port))
        self._set_entry(self.key_entry, key)
        self._set_entry(self.hash_entry, hash_)

    def _set_entry(self, entry, value):
        entry.config(state='normal')
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state='readonly')

    def _set_text(self, text_widget, value):
        text_widget.config(state='normal')
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, value)
        text_widget.config(state='disabled')
