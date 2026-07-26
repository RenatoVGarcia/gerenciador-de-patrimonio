import yfinance as yf

def buscar_cotacao_b3(ticker_input):
    """
    Busca as informações e preço atualizado de uma ação ou FII da B3.
    Retorna um dicionário com os dados ou levanta uma exceção se falhar.
    """
    ticker_clean = ticker_input.strip().upper()
    if not ticker_clean:
        raise ValueError("O código do ticker não pode estar vazio.")

    # Se não tiver extensão .SA (padrão B3 no Yahoo Finance), adiciona automaticamente
    ticker_search = ticker_clean if ticker_clean.endswith(".SA") else f"{ticker_clean}.SA"

    ativo = yf.Ticker(ticker_search)
    info = ativo.info

    # Tenta obter o preço em tempo real / fechamento
    preco = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
    nome_empresa = info.get("shortName") or info.get("longName") or ticker_clean

    if preco is None:
        raise ValueError("Preço não localizado. Verifique se o ticker é válido na B3.")

    # Identificação simples de tipo (FIIs geralmente terminam com 11 e possuem 6 caracteres)
    tipo = "FII" if "11" in ticker_clean and not ticker_clean.startswith("11") else "Ação"

    return {
        "ticker": ticker_clean,
        "nome": nome_empresa,
        "preco": float(preco),
        "tipo": tipo
    }