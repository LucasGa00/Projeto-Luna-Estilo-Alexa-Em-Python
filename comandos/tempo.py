from datetime import datetime, timedelta
from voz import falar

def informar_previsao(cidade="São Paulo", dias=1):
    # Dicionário para traduzir dias da semana do inglês para português
    dias_semana_pt = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    # Tratar caso dias seja "semana"
    if dias == "semana":
        dias = 7

    # Calcular data alvo
    try:
        data_alvo = datetime.now() + timedelta(days=dias - 1)
    except Exception as e:
        falar("Houve um erro ao calcular a data da previsão.")
        print(f"Erro: {e}")
        return

    nome_dia_ingles = data_alvo.strftime('%A')
    nome_dia_pt = dias_semana_pt.get(nome_dia_ingles, nome_dia_ingles)
    data_formatada = data_alvo.strftime("%d/%m/%Y")

    # Simular dados da previsão (substitua pela API real quando quiser)
    previsao_simulada = {
        "min": 12.7,
        "max": 24.5,
        "vento": 17.8,
        "descricao": "garoa"
    }

    # Construir mensagem amigável para falar
    msg = (
        f"Aqui está a previsão para {cidade} em {nome_dia_pt}, {data_formatada}. "
        f"A temperatura mínima será de {previsao_simulada['min']} graus, "
        f"a máxima de {previsao_simulada['max']} graus. "
        f"Ventania de até {previsao_simulada['vento']:.1f} quilômetros por hora, "
        f"com {previsao_simulada['descricao']}. Fique preparado!"
    )

    falar(msg)
    print(msg)
