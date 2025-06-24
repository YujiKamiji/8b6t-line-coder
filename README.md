# 8B6T Line Coder – Comunicação Segura via Sockets TCP

Este é o projeto final da disciplina **Comunicação de Dados**, que simula um sistema completo de transmissão de mensagens entre dois computadores em uma rede local. O sistema combina:

- **Codificação de linha 8B6T** para representar os dados como sinais ternários
- **Criptografia AES-256-GCM** para garantir sigilo e integridade
- **Sockets TCP** para comunicação confiável entre cliente e servidor
- (Opcional) **Interface gráfica** para visualização do processo e da forma de onda

---

## 🧩 Funcionalidades

- Envio e recebimento de mensagens em tempo real
- Codificação e decodificação automática no formato 8B6T
- Criptografia segura com chave simétrica AES-GCM (com IV e tag)
- Comunicação entre dispositivos distintos em uma mesma rede Wi-Fi
- Modularização em Python com suporte multiplataforma (Windows/Linux)

---

## 🛠 Requisitos

- Python 3.10 ou superior
-Instale as dependências com:

```bash
pip install -r requirements.txt
```
## Créditos

Para a implementação da lógica de codificação, utilizamos uma tabela de mapeamento 8B6T de um projeto de código aberto. Todos os créditos por este trabalho de compilação de dados vão para seus respectivos autores.

* **Recurso:** Tabela de Mapeamento 8B6T
* **Projeto Original:** [Multilevel-Line-Encoding](https://github.com/CSE-Projects/Multilevel-Line-Encoding.git)
* **Autores:**
    * [Omkar Prabhu (omkarprabhu-98)](https://github.com/omkarprabhu-98)
    * [Dibyadarshan Hota (Dibyadarshan)](https://github.com/Dibyadarshan)
