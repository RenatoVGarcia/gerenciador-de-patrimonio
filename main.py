import tkinter as tk
from database import Database
from gui import InvestAppGUI

def main():
    # Inicializa a camada de banco de dados
    db = Database("investimentos.db")

    # Inicializa a interface gráfica
    root = tk.Tk()
    app = InvestAppGUI(root, db)
    
    # Roda a aplicação
    root.mainloop()

if __name__ == "__main__":
    main()