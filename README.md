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
```

### 2. Criar e Ativar o Ambiente Virtual (Recomendado)

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```
Nota: O projeto utiliza módulos padrão do Python (tkinter, sqlite3, urllib, json, datetime). Caso utilize bibliotecas externas de busca como requests ou beautifulsoup4, certifique-se de adicioná-las no comando acima.

### 4. Executar a Aplicação

```bash
python main.py
```

## 📂 Estrutura do Projeto

gerenciador-de-patrimonio/
│
├── database.py       # Gerenciamento das tabelas e conexões do SQLite
├── b3_service.py     # Integração/scraping de cotações da B3 (Ações e FIIs)
├── bcb_service.py    # Consulta de Selic/CDI na API do Banco Central + Cálculo de IR
├── gui.py            # Interface gráfica com Tkinter e regras de exibição
├── main.py           # Ponto de entrada (script de inicialização)
├── requirements.txt  # Lista de dependências do projeto
└── README.md         # Documentação do projeto


## 📖 Como Usar

---

### 📈 Cadastrando Ações e FIIs (Renda Variável)

1. Clique no menu **☰ Menu** no canto superior esquerdo.
2. Selecione a opção **🔍 Buscar Ativo B3 (Ações/FIIs)**.
3. Digite o ticker do papel desejado (ex: `ITUB4`, `PETR4`, `MXRF11`) e clique em **Buscar**.
4. O sistema trará a cotação atualizada automaticamente. Confirme o preço pago e a quantidade comprada.
5. Clique em **⚡ Salvar na Carteira**.

> **Nota:** Se você já possuir esse ativo, o aplicativo recalculará o seu **Preço Médio (PM)** e a quantidade total automaticamente!

---

### 💰 Cadastrando Renda Fixa (CDB, LCI, LCA, Tesouro Direto)

1. Clique no menu **☰ Menu** > **➕ Inserir Novo Investimento**.
2. No campo **Tipo**, escolha **Renda Fixa** ou **Tesouro Direto**.
3. Preencha o nome identificador do título (ex: `CDB Banco Inter 110% CDI` ou `LCA Banco do Brasil 90% CDI`).
4. Informe o valor total aplicado, a porcentagem da taxa (ex: `110`), o indexador (`CDI`, `Pré`, `IPCA`), a data do aporte e o vencimento.
5. Clique em **💾 Salvar Investimento**.

> **Dica:** Ativos que contenham `LCI` ou `LCA` no nome terão a alíquota de Imposto de Renda ajustada para **0,0% (Isento)** de forma automática.

---

### 👁️ Recursos de Interface

* **Modo Privacidade:** Clique no botão **👁️ Ocultar Valores** no topo da tela para mascarar os saldos reais sempre que for tirar prints ou gravar a tela.
* **Filtro Rápido:** Use o seletor **🔍 Categoria** para isolar apenas Ações, FIIs ou Renda Fixa na tabela.
* **Exclusão:** Selecione qualquer linha da tabela e clique em **🗑️ Excluir Selecionado** para remover o ativo do banco de dados.

---

## 📊 Regras de Negócio e Tributação

A aplicação calcula o desconto do Imposto de Renda Regressivo com base no número de dias decorridos desde a data do aporte:

| Tempo Decorrido (Dias) | Alíquota de IR |
| :--- | :---: |
| Até 180 dias | 22,5% |
| De 181 a 360 dias | 20,0% |
| De 361 a 720 dias | 17,5% |
| Acima de 720 dias | 15,0% |

> ⚠️ **Isenção Fiscal:** Qualquer título contendo os termos **LCI** ou **LCA** no nome é tratado automaticamente com alíquota **0,0% (Isento)**.

---

## 📄 Licença

Este projeto é um software de código aberto (*open-source*) distribuído sob os termos da **Licença MIT**.

```Plaintext
MIT License

Copyright (c) Renato V. Garcia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
