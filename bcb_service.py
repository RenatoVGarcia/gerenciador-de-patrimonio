import urllib.request
import json
from datetime import datetime

def buscar_selic_atual():
    """Busca a taxa Selic diária acumulada/anualizada na API oficial do Banco Central."""
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return float(data[0]['valor'])
    except Exception:
        return 10.50  # Valor fallback padronizado caso fique sem internet

def calcular_aliquota_ir(dias_corridos, eh_isento=False):
    """Retorna a alíquota de IR da tabela regressiva da Renda Fixa."""
    if eh_isento:
        return 0.0
    if dias_corridos <= 180:
        return 0.225
    elif dias_corridos <= 360:
        return 0.200
    elif dias_corridos <= 720:
        return 0.175
    else:
        return 0.150

def calcular_rendimento_renda_fixa(valor_aplicado, data_aporte_str, taxa_percentual, indexador, eh_isento=False):
    """Estima o valor atual bruto e líquido com base nos dias decorridos e na taxa Selic/CDI."""
    try:
        data_aporte = datetime.strptime(data_aporte_str, "%d/%m/%Y")
        dias_decorridos = (datetime.now() - data_aporte).days
        if dias_decorridos <= 0:
            return valor_aplicado, valor_aplicado, 0.0

        taxa_selic_ano = buscar_selic_atual() / 100.0

        # Ajusta taxa anual conforme o indexador
        if indexador == "CDI":
            taxa_anual_efetiva = taxa_selic_ano * (taxa_percentual / 100.0)
        elif indexador == "Pré":
            taxa_anual_efetiva = taxa_percentual / 100.0
        else: # IPCA ou outro
            taxa_anual_efetiva = 0.045 + (taxa_percentual / 100.0)

        # Cálculo de juros simples proporcional aos dias (aprox.)
        rendimento_bruto = valor_aplicado * (taxa_anual_efetiva * (dias_decorridos / 365.0))
        valor_bruto = valor_aplicado + rendimento_bruto

        # Cálculo do Imposto de Renda
        aliquota_ir = calcular_aliquota_ir(dias_decorridos, eh_isento)
        imposto = rendimento_bruto * aliquota_ir
        valor_liquido = valor_bruto - imposto

        return valor_bruto, valor_liquido, aliquota_ir
    except Exception:
        return valor_aplicado, valor_aplicado, 0.0
