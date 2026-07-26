# 📈 Gerenciador de Carteira de Investimentos

Um aplicativo desktop simples, moderno e completo em Python para acompanhamento de patrimônio, integrando ativos de **Renda Variável (Ações e FIIs)** com cotações da B3 e **Renda Fixa (CDBs, LCIs, LCAs, Tesouro Direto)** com rendimento diário automático e desconto de Imposto de Renda Regressivo.

---

## 🚀 Funcionalidades

### 📈 Renda Variável (Ações e FIIs)
- **Busca via API B3:** Consulta de cotações em tempo real digitando apenas o ticker do ativo (ex: `PETR4`, `VALE3`, `MXRF11`).
- **Recálculo do Preço Médio (PM):** Atualiza automaticamente a posição e o preço médio a cada novo aporte.
- **Resultado Atualizado:** Exibe ganhos/perdas absolutos com base na cotação de mercado.

### 💰 Renda Fixa (CDB, LCI, LCA, Tesouro)
- **Cálculo Automático de Rendimento:** Integração com a API do Banco Central do Brasil para puxar a taxa Selic/CDI atualizada.
- **Atrelado a Diversos Indexadores:** Suporte a ativos atrelados ao **CDI**, **Pré-fixados**, **IPCA** ou **Selic**.
- **Imposto de Renda Regressivo:** Aplicação automática da tabela regressiva do IR (22,5% a 15,0%) sobre os lucros de CDBs e Tesouro.
- **Isenção Inteligente:** Identificação automática de títulos isentos (LCI e LCA).
- **Controle de Vencimentos:** Exibição da data final do contrato na carteira.

### 🛡️ Usabilidade e Interface
- **Modo Privacidade:** Oculte os valores monetários com um clique para mostrar a tela sem expor o patrimônio (`👁️ Ocultar Valores`).
- **Filtro por Categoria:** Visualize apenas Ações, FIIs ou Renda Fixa com facilidade.
- **Interface Gráfica Nativa (Tkinter):** Leve, sem necessidade de navegador.
- **Banco de Dados SQLite Local:** Seus dados financeiros salvos com total privacidade no seu computador.

---

## 📂 Estrutura do Projeto

```text
├── database.py       # Gerenciamento das tabelas e conexões do SQLite
├── b3_service.py     # Integração/scraping de cotações da B3 (Ações e FIIs)
├── bcb_service.py    # Consulta de Selic/CDI na API do Banco Central + Cálculo de IR
├── gui.py            # Interface gráfica com Tkinter e regras de exibição
└── main.py           # Ponto de entrada (script de inicialização)
