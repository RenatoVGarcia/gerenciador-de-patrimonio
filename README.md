# 📈 Gerenciador de Carteira de Investimentos

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Um aplicativo desktop simples, moderno e completo em Python para acompanhamento de patrimônio, integrando ativos de **Renda Variável (Ações e FIIs)** com cotações da B3 e **Renda Fixa (CDBs, LCIs, LCAs, Tesouro Direto)** com rendimento diário automático e desconto de Imposto de Renda Regressivo.

---

## 📌 Sumário

- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Usar](#-como-usar)
- [Regras de Negócio e Tributação](#-regras-de-negócio-e-tributação)
- [Licença](#-licença)

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

## 📋 Pré-requisitos

Antes de começar, você precisará das seguintes ferramentas instaladas em seu computador:

- **[Python 3.8+](https://www.python.org/downloads/)**
- **[Git](https://git-scm.com/)** *(opcional, para clonar o repositório)*
- Conexão ativa com a **Internet** (necessária para atualização de cotações da B3 e dados do Banco Central).

---

## 📦 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone [https://github.com/RenatoVGarcia/gerenciador-de-patrimonio.git](https://github.com/RenatoVGarcia/gerenciador-de-patrimonio.git)
cd gerenciador-de-patrimonio
