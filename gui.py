import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
from b3_service import buscar_cotacao_b3
from bcb_service import calcular_rendimento_renda_fixa

class InvestAppGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        
        self.root.title("Controle de Investimentos - Ações & Renda Fixa")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f9")

        self.valores_ocultos = False

        self.setup_header()
        self.setup_carteira_view()

        self.load_data()
        self.atualizar_cotacoes_async()

    # ==================== CABEÇALHO ====================
    def setup_header(self):
        header_frame = tk.Frame(self.root, bg="#1e293b", height=50)
        header_frame.pack(fill="x", side="top")

        btn_menu = tk.Button(
            header_frame, text="☰ Menu", font=("Arial", 11, "bold"), 
            bg="#1e293b", fg="white", bd=0, activebackground="#334155", activeforeground="white",
            command=self.show_menu
        )
        btn_menu.pack(side="left", padx=10, pady=8)

        self.popup_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="🔍 Buscar Ativo B3 (Ações/FIIs)", command=self.open_window_busca)
        self.popup_menu.add_command(label="➕ Inserir Novo Investimento", command=self.open_window_manual)

        lbl_titulo = tk.Label(header_frame, text="Minha Carteira", font=("Arial", 13, "bold"), bg="#1e293b", fg="white")
        lbl_titulo.pack(side="left", padx=10)

        btn_atualizar = tk.Button(
            header_frame, text="🔄 Atualizar Mercado", font=("Arial", 9, "bold"),
            bg="#0284c7", fg="white", bd=0, activebackground="#0369a1", activeforeground="white",
            padx=10, pady=3, command=self.atualizar_cotacoes_async
        )
        btn_atualizar.pack(side="right", padx=10, pady=8)

        self.btn_ocultar = tk.Button(
            header_frame, text="👁️ Ocultar Valores", font=("Arial", 9, "bold"),
            bg="#334155", fg="white", bd=0, activebackground="#475569", activeforeground="white",
            padx=10, pady=3, command=self.toggle_privacidade
        )
        self.btn_ocultar.pack(side="right", padx=5, pady=8)

    def show_menu(self):
        try:
            self.popup_menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            self.popup_menu.grab_release()

    def toggle_privacidade(self):
        self.valores_ocultos = not self.valores_ocultos
        self.btn_ocultar.config(text="🙈 Mostrar Valores" if self.valores_ocultos else "👁️ Ocultar Valores")
        self.load_data()

    # ==================== VISUALIZAÇÃO PRINCIPAL ====================
    def setup_carteira_view(self):
        top_bar = tk.Frame(self.root, bg="#f4f6f9")
        top_bar.pack(fill="x", padx=15, pady=(15, 5))

        tk.Label(top_bar, text="🔍 Categoria:", font=("Arial", 10, "bold"), bg="#f4f6f9").pack(side="left", padx=(0, 5))
        
        self.combo_filtro = ttk.Combobox(
            top_bar, values=["Todos", "Ação", "Renda Fixa", "FII", "Tesouro Direto", "Cripto", "Outro"], 
            width=15, state="readonly"
        )
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side="left")
        self.combo_filtro.bind("<<ComboboxSelected>>", lambda event: self.load_data())

        self.lbl_status_cotacao = tk.Label(top_bar, text="", font=("Arial", 9, "italic"), bg="#f4f6f9", fg="#64748b")
        self.lbl_status_cotacao.pack(side="left", padx=15)

        btn_del = tk.Button(top_bar, text="🗑️ Excluir Selecionado", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), command=self.delete_investment)
        btn_del.pack(side="right")

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Tabela expansível cobrindo tanto Ações quanto Renda Fixa
        cols = ("ID", "Ativo/Emissor", "Tipo", "Taxa/Index", "Qtd", "PM / Aplicado", "Val. Atual (Líq)", "Resultado", "Vencimento")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

        widths = [35, 150, 90, 100, 50, 110, 110, 100, 100]
        for col, width in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.lbl_total = tk.Label(self.root, text="Patrimônio Total: R$ 0,00", font=("Arial", 12, "bold"), bg="#f4f6f9", fg="#1e293b")
        self.lbl_total.pack(anchor="e", padx=20, pady=10)

    # ==================== PROCESSAMENTO EM SEGUNDO PLANO ====================
    def atualizar_cotacoes_async(self):
        threading.Thread(target=self._atualizar_cotacoes_process, daemon=True).start()

    def _atualizar_cotacoes_process(self):
        self.lbl_status_cotacao.config(text="⏳ Atualizando valores de mercado e cotações...")
        investimentos = self.db.listar_todos()

        for item in investimentos:
            item_id, nome, tipo = item[0], item[1], item[2]
            
            if tipo in ["Ação", "FII"]:
                ticker = nome.split(" ")[0].upper()
                try:
                    dados = buscar_cotacao_b3(ticker)
                    if dados and "preco" in dados and dados["preco"] > 0:
                        self.db.atualizar_preco_atual(item_id, dados["preco"])
                except Exception:
                    pass

        self.lbl_status_cotacao.config(text="✅ Dados atualizados!")
        self.root.after(0, self.load_data)

    # ==================== MODAL DE CADASTRO UNIFICADO ====================
    def open_window_manual(self):
        win = tk.Toplevel(self.root)
        win.title("Cadastrar Investimento")
        win.geometry("420x450")
        win.resizable(False, False)
        win.grab_set()

        form = tk.Frame(win, padx=15, pady=15)
        form.pack(fill="both", expand=True)

        # Campos gerais
        tk.Label(form, text="Tipo:").grid(row=0, column=0, sticky="w", pady=4)
        combo_tipo = ttk.Combobox(form, values=["Ação", "Renda Fixa", "FII", "Tesouro Direto", "Cripto", "Outro"], width=22, state="readonly")
        combo_tipo.set("Renda Fixa")
        combo_tipo.grid(row=0, column=1, pady=4)

        tk.Label(form, text="Ativo/Nome:").grid(row=1, column=0, sticky="w", pady=4)
        ent_nome = tk.Entry(form, width=25)
        ent_nome.insert(0, "")
        ent_nome.grid(row=1, column=1, pady=4)

        tk.Label(form, text="Quantidade:").grid(row=2, column=0, sticky="w", pady=4)
        ent_qtd = tk.Entry(form, width=25)
        ent_qtd.insert(0, "")
        ent_qtd.grid(row=2, column=1, pady=4)

        tk.Label(form, text="Preço Unit. / Valor (R$):").grid(row=3, column=0, sticky="w", pady=4)
        ent_preco = tk.Entry(form, width=25)
        ent_preco.grid(row=3, column=1, pady=4)

        # Campos específicos de Renda Fixa
        tk.Label(form, text="Indexador:").grid(row=4, column=0, sticky="w", pady=4)
        combo_index = ttk.Combobox(form, values=["CDI", "Pré", "IPCA", "Selic"], width=22, state="readonly")
        combo_index.set("CDI")
        combo_index.grid(row=4, column=1, pady=4)

        tk.Label(form, text="Taxa (% ex: 110 ou 12.5):").grid(row=5, column=0, sticky="w", pady=4)
        ent_taxa = tk.Entry(form, width=25)
        ent_taxa.insert(0, "")
        ent_taxa.grid(row=5, column=1, pady=4)

        tk.Label(form, text="Vencimento (DD/MM/AAAA):").grid(row=6, column=0, sticky="w", pady=4)
        ent_venc = tk.Entry(form, width=25)
        ent_venc.insert(0, "")
        ent_venc.grid(row=6, column=1, pady=4)

        tk.Label(form, text="Data Aporte:").grid(row=7, column=0, sticky="w", pady=4)
        ent_data = tk.Entry(form, width=25)
        ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        ent_data.grid(row=7, column=1, pady=4)

        def salvar():
            try:
                nome = ent_nome.get().strip()
                tipo = combo_tipo.get()
                qtd = float(ent_qtd.get().replace(",", "."))
                preco = float(ent_preco.get().replace(",", "."))
                taxa = ent_taxa.get().strip()
                indexador = combo_index.get()
                vencimento = ent_venc.get().strip()
                data = ent_data.get().strip()

                if not nome:
                    messagebox.showwarning("Erro", "Nome/Ativo é obrigatório!", parent=win)
                    return

                self.db.adicionar_ou_atualizar(
                    nome=nome, tipo=tipo, quantidade_nova=qtd, preco_novo=preco, 
                    taxa=taxa, data_aporte=data, indexador=indexador, vencimento=vencimento
                )

                win.destroy()
                self.load_data()
                messagebox.showinfo("Sucesso", "Investimento registrado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade e Preço devem ser números!", parent=win)

        btn_salvar = tk.Button(form, text="💾 Salvar Investimento", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=salvar)
        btn_salvar.grid(row=8, column=0, columnspan=2, pady=15)

    def open_window_busca(self):
        win_busca = tk.Toplevel(self.root)
        win_busca.title("Buscar Ativo B3")
        win_busca.geometry("450x380")
        win_busca.resizable(False, False)
        win_busca.grab_set()

        search_frame = tk.Frame(win_busca, padx=15, pady=15)
        search_frame.pack(fill="both", expand=True)

        tk.Label(search_frame, text="Ticker (ex: VALE3, PETR4, MXRF11):", font=("Arial", 9, "bold")).pack(anchor="w")

        input_box = tk.Frame(search_frame)
        input_box.pack(fill="x", pady=5)

        ent_busca_ticker = tk.Entry(input_box, font=("Arial", 11), width=15)
        ent_busca_ticker.pack(side="left", padx=(0, 10))

        lbl_info_ativo = tk.Label(search_frame, text="Digite um ticker e clique em Buscar.", font=("Arial", 10), justify="left", pady=10)
        lbl_info_ativo.pack(anchor="w")

        buy_frame = tk.Frame(search_frame)

        tk.Label(buy_frame, text="Qtd Comprada:").grid(row=0, column=0, sticky="w", pady=5)
        ent_busca_qtd = tk.Entry(buy_frame, width=12)
        ent_busca_qtd.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(buy_frame, text="Preço Pago (R$):").grid(row=1, column=0, sticky="w", pady=5)
        ent_busca_preco = tk.Entry(buy_frame, width=12)
        ent_busca_preco.grid(row=1, column=1, padx=5, pady=5)

        ativo_atual = {}

        def pesquisar():
            nonlocal ativo_atual
            ticker_input = ent_busca_ticker.get()
            if not ticker_input.strip():
                return

            try:
                lbl_info_ativo.config(text="Buscando na B3...")
                win_busca.update_idletasks()

                dados = buscar_cotacao_b3(ticker_input)
                ativo_atual = dados

                lbl_info_ativo.config(
                    text=f"📌 {dados['ticker']} - {dados['nome']}\n"
                         f"🏷️ Tipo: {dados['tipo']}\n"
                         f"💡 Cotação Automática: R$ {dados['preco']:.2f}"
                )

                ent_busca_preco.delete(0, tk.END)
                ent_busca_preco.insert(0, f"{dados['preco']:.2f}")

                buy_frame.pack(anchor="w", pady=10)
            except Exception as e:
                lbl_info_ativo.config(text=f"❌ Erro: {str(e)}")

        def confirmar_compra():
            if not ativo_atual:
                return

            try:
                qtd = float(ent_busca_qtd.get().replace(",", "."))
                preco_pago = float(ent_busca_preco.get().replace(",", "."))

                nome = f"{ativo_atual['ticker']} ({ativo_atual['nome']})"
                tipo = ativo_atual['tipo']
                data = datetime.now().strftime("%d/%m/%Y")

                self.db.adicionar_ou_atualizar(nome, tipo, qtd, preco_pago, "B3", data)

                win_busca.destroy()
                self.load_data()
                self.atualizar_cotacoes_async()
                messagebox.showinfo("Sucesso!", "Ativo adicionado e PM recalculado!")
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos.")

        btn_pesquisar = tk.Button(input_box, text="🔍 Buscar", bg="#007bff", fg="white", font=("Arial", 9, "bold"), command=pesquisar)
        btn_pesquisar.pack(side="left")

        btn_confirmar = tk.Button(buy_frame, text="⚡ Salvar na Carteira", bg="#28a745", fg="white", font=("Arial", 9, "bold"), command=confirmar_compra)
        btn_confirmar.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

    # ==================== RENDERIZAÇÃO DA TABELA ====================
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = self.combo_filtro.get() if hasattr(self, 'combo_filtro') else "Todos"
        rows = self.db.listar_todos(tipo_filtro=filtro)
        
        patrimonio_total = 0.0

        for row in rows:
            # Desempacotamento de dados
            item_id, nome, tipo, qtd, pm, total_investido, taxa_str, data_aporte = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
            preco_atual_b3 = row[8] if len(row) > 8 else pm
            indexador = row[9] if len(row) > 9 and row[9] else "CDI"
            vencimento = row[10] if len(row) > 10 and row[10] else "-"

            # Cálculo individual por tipo de ativo
            if tipo in ["Renda Fixa", "Tesouro Direto"]:
                isento = "LCI" in nome.upper() or "LCA" in nome.upper()
                try:
                    taxa_val = float(taxa_str.replace("%", "").replace(",", "."))
                except ValueError:
                    taxa_val = 100.0

                bruto, liquido, aliquota = calcular_rendimento_renda_fixa(
                    valor_aplicado=total_investido, data_aporte_str=data_aporte,
                    taxa_percentual=taxa_val, indexador=indexador, eh_isento=isento
                )
                valor_posicao = liquido
                resultado = valor_posicao - total_investido
                taxa_exibicao = f"{taxa_str}% {indexador}"
            else:
                # Ações, FIIs, etc.
                p_atual = preco_atual_b3 if preco_atual_b3 > 0 else pm
                valor_posicao = qtd * p_atual
                resultado = valor_posicao - (qtd * pm)
                taxa_exibicao = "-"

            patrimonio_total += valor_posicao

            # Formatação de privacidade
            if self.valores_ocultos:
                qtd_s, pm_s, val_atual_s, res_s = "***", "R$ ***", "R$ ***", "R$ ***"
            else:
                qtd_s = f"{qtd:.2f}"
                pm_s = f"R$ {pm:.2f}"
                val_atual_s = f"R$ {valor_posicao:.2f}"
                sinal = "+" if resultado >= 0 else ""
                res_s = f"{sinal}R$ {resultado:.2f}"

            self.tree.insert("", "end", values=(
                item_id, nome, tipo, taxa_exibicao, qtd_s,
                pm_s, val_atual_s, res_s, vencimento
            ))

        if self.valores_ocultos:
            self.lbl_total.config(text="Patrimônio Total: R$ ***")
        else:
            self.lbl_total.config(text=f"Patrimônio Total Estimado: R$ {patrimonio_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    def delete_investment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um item.")
            return

        item_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Excluir registro #{item_id}?"):
            self.db.deletar(item_id)
            self.load_data()
