import tkinter as tk
from .client_interface import ClientScreen
from .server_interface import ServerScreen

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8B6T Comunicação Segura")
        self.geometry("800x600")

        self.current_screen = None
        self.show_initial_screen()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_initial_screen(self):
        self.clear_screen()

        frame = tk.Frame(self)
        frame.pack(expand=True)

        tk.Label(frame, text="Escolha o modo de operação:", font=("Arial", 18)).pack(pady=30)

        tk.Button(frame, text="Cliente (Enviar Mensagem)", font=("Arial", 14), width=30, height=2,
                  command=self.show_client_screen).pack(pady=15)

        tk.Button(frame, text="Servidor (Receber Mensagem)", font=("Arial", 14), width=30, height=2,
                  command=self.show_server_screen).pack(pady=15)

        self.current_screen = frame

    def show_client_screen(self):
        self.clear_screen()
        self.current_screen = ClientScreen(self, on_back=self.show_initial_screen)
        self.current_screen.pack(fill="both", expand=True)

    def show_server_screen(self):
        self.clear_screen()
        self.current_screen = ServerScreen(self, on_back=self.show_initial_screen)
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
