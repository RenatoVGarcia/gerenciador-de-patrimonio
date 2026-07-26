import sqlite3

class Database:
    def __init__(self, db_name="investimentos.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Inicializa a tabela de investimentos no SQLite com suporte a Renda Fixa detalhada."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS investimentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    quantidade REAL NOT NULL,
                    preco_unitario REAL NOT NULL,
                    total REAL NOT NULL,
                    taxa TEXT,
                    data_aporte TEXT NOT NULL,
                    preco_atual REAL DEFAULT 0.0,
                    indexador TEXT DEFAULT 'CDI',
                    vencimento TEXT DEFAULT '',
                    emissor TEXT DEFAULT ''
                )
            """)
            conn.commit()

    def adicionar_ou_atualizar(self, nome, tipo, quantidade_nova, preco_novo, taxa, data_aporte, indexador="CDI", vencimento="", emissor=""):
        """Adiciona ou atualiza investimento recalculando o Preço Médio/Aporte Total."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, quantidade, total FROM investimentos WHERE LOWER(nome) = LOWER(?)", (nome.strip(),))
            ativo_existente = cursor.fetchone()

            if ativo_existente:
                item_id, qtd_antiga, total_antigo = ativo_existente
                nova_qtd = qtd_antiga + quantidade_nova
                novo_total = total_antigo + (quantidade_nova * preco_novo)
                novo_preco_medio = novo_total / nova_qtd if nova_qtd > 0 else 0

                cursor.execute("""
                    UPDATE investimentos 
                    SET quantidade = ?, preco_unitario = ?, total = ?, taxa = ?, data_aporte = ?, 
                        preco_atual = ?, indexador = ?, vencimento = ?, emissor = ?
                    WHERE id = ?
                """, (nova_qtd, novo_preco_medio, novo_total, taxa, data_aporte, preco_novo, indexador, vencimento, emissor, item_id))
            else:
                total_novo = quantidade_nova * preco_novo
                cursor.execute("""
                    INSERT INTO investimentos (nome, tipo, quantidade, preco_unitario, total, taxa, data_aporte, preco_atual, indexador, vencimento, emissor)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (nome.strip(), tipo, quantidade_nova, preco_novo, total_novo, taxa, data_aporte, preco_novo, indexador, vencimento, emissor))
            
            conn.commit()

    def atualizar_preco_atual(self, item_id, preco_atual):
        """Atualiza apenas a cotação/valor atual de um ativo."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE investimentos SET preco_atual = ? WHERE id = ?", (preco_atual, item_id))
            conn.commit()

    def listar_todos(self, tipo_filtro="Todos"):
        """Retorna os investimentos cadastrados."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if tipo_filtro == "Todos" or not tipo_filtro:
                cursor.execute("SELECT * FROM investimentos ORDER BY id DESC")
            else:
                cursor.execute("SELECT * FROM investimentos WHERE tipo = ? ORDER BY id DESC", (tipo_filtro,))
            return cursor.fetchall()

    def deletar(self, item_id):
        """Exclui um registro pelo ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM investimentos WHERE id = ?", (item_id,))
            conn.commit()