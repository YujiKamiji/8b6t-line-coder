import tkinter as tk
from .client_interface import ClientScreen
from .server_interface import ServerScreen

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8B6T Comunicação Segura")
        self.geometry("800x600")
        self.resizable(False, False)

        self.current_screen = None
        self.show_initial_screen()

    def clear_screen(self):
        """Remove a tela atual da janela"""
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None

    def show_initial_screen(self):
        """Mostra a tela inicial com as opções de modo"""
        self.clear_screen()

        frame = tk.Frame(self)
        frame.pack(expand=True)

        title = tk.Label(frame, text="Escolha o modo de operação:", font=("Arial", 18))
        title.pack(pady=30)

        client_button = tk.Button(
            frame,
            text="Cliente (Enviar Mensagem)",
            font=("Arial", 14),
            width=30,
            height=2,
            command=self.show_client_screen
        )
        client_button.pack(pady=15)

        server_button = tk.Button(
            frame,
            text="Servidor (Receber Mensagem)",
            font=("Arial", 14),
            width=30,
            height=2,
            command=self.show_server_screen
        )
        server_button.pack(pady=15)

        self.current_screen = frame

    def show_client_screen(self):
        """Alterna para a tela de cliente"""
        self.clear_screen()
        self.current_screen = ClientScreen(master=self, on_back=self.show_initial_screen)
        self.current_screen.pack(fill="both", expand=True)

    def show_server_screen(self):
        """Alterna para a tela de servidor"""
        self.clear_screen()
        self.current_screen = ServerScreen(master=self, on_back=self.show_initial_screen)
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
