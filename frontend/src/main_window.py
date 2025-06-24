import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("8B6T Line Coder - Escolha de Modo")
        self.root.geometry("400x200")

        # Label
        label = ttk.Label(root, text="Escolha o modo de operacão:", font=("Arial", 14))
        label.pack(pady=20)

        # Botões
        cliente_btn = ttk.Button(root, text="Cliente (Enviar)", command=self.ir_para_cliente)
        cliente_btn.pack(pady=10)

        servidor_btn = ttk.Button(root, text="Servidor (Receber)", command=self.ir_para_servidor)
        servidor_btn.pack(pady=10)

    def ir_para_cliente(self):
        print("Abrir tela do cliente")
        # Aqui você futuramente chamaria a interface do cliente

    def ir_para_servidor(self):
        print("Abrir tela do servidor")
        # Aqui você futuramente chamaria a interface do servidor

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
