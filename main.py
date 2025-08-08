import re
from voz import falar, ouvir
import comandos.luz as luz
import comandos.tempo as tempo
from ia import responder_pergunta
from datetime import datetime, timedelta

ultima_resposta_ia = None

def contem_palavra(palavra, texto):
    texto = texto.lower()
    padrao = rf"\b{re.escape(palavra)}\b"
    return re.search(padrao, texto) is not None

def contem_qualquer_palavra(palavras, texto):
    texto = texto.lower()
    for palavra in palavras:
        padrao = rf"\b{re.escape(palavra)}\b"
        if re.search(padrao, texto):
            return True
    return False

falar("Olá! Sou a Luna, sua assistente virtual. Diga 'Luna' para começar.")

estado_pendente = None  # Memória de curto prazo

while True:
    comando = ouvir()
    if comando == "":
        continue

    comando = comando.strip().lower()
    print(f"Você disse: {comando}")

    # Só processa se começar com "luna"
    if not comando.startswith("luna"):
        # Não reconheceu, mas não responde nada
        continue

    # Remove o gatilho "luna" para processar o resto do comando
    comando = comando[len("luna"):].strip()

    # Comando para repetir a última resposta da IA
    if "repita isso" in comando or "repita" in comando:
        if ultima_resposta_ia:
            falar(ultima_resposta_ia)
        else:
            falar("Ainda não tenho nada para repetir.")
        continue

    reconheceu = False
    partes = re.split(r'\be\b|\bou\b|,', comando)
    acoes = []

    palavras_hora = [
        "hora", "horas", "horário", "que horas", "qual o horário", "qual a hora",
        "me diga a hora", "me informe a hora", "me fala a hora"
    ]

    palavras_data_hoje = ["hoje"]
    palavras_data_geral = [
        "data", "dia", "qual a data", "me diga a data", "me informe a data"
    ]

    palavras_ligar = ["ligar", "ligue", "acender", "acenda"]
    palavras_desligar = ["desligar", "desligue", "apagar", "apague", "desliga"]
    palavras_luz = ["luz", "a luz", "luz do quarto", "a luz do quarto"]

    palavras_cronometro = ["cronômetro", "cronometro"]
    palavras_parar = ["parar", "cancela", "interrompe"]
    palavras_tempo_restante = ["quanto", "resta", "falta", "tempo restante"]


    if estado_pendente == "esperando_objeto_para_ligar":
        if contem_qualquer_palavra(palavras_luz, comando):
            acoes.append(("falar", "Ligando a luz."))
            acoes.append(("print", "🔦 Luz ligada."))
            acoes.append(("acao", luz.ligar))
            estado_pendente = None
        else:
            acoes.append(("falar", "Desculpe, não entendi o que ligar. Pode repetir?"))
        for tipo, valor in acoes:
            if tipo == "falar":
                falar(valor)
            elif tipo == "print":
                print(valor)
            elif tipo == "acao":
                valor()
        continue

    if estado_pendente == "esperando_objeto_para_desligar":
        if contem_qualquer_palavra(palavras_luz, comando):
            acoes.append(("falar", "Desligando a luz."))
            acoes.append(("print", "🔦 Luz desligada."))
            acoes.append(("acao", luz.desligar))
            estado_pendente = None
        else:
            acoes.append(("falar", "Desculpe, não entendi o que desligar. Pode repetir?"))
        for tipo, valor in acoes:
            if tipo == "falar":
                falar(valor)
            elif tipo == "print":
                print(valor)
            elif tipo == "acao":
                valor()
        continue

    dias_semana = {
        "segunda": 0,
        "terça": 1, "terca": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
        "sábado": 5, "sabado": 5,
        "domingo": 6
    }

    hoje = datetime.now()
    dia_atual = hoje.weekday()

    # Variáveis para controle e evitar repetição
    falou_data = False
    falou_hora = False

    for parte in partes:
        parte = parte.strip()

        if contem_palavra("previsão", parte) or contem_palavra("clima", parte) or contem_palavra("tempo", parte):
            reconheceu = True
            previsao_adicionada = False

            if contem_palavra("semana", parte):
                acoes.append(("acao", lambda: tempo.informar_previsao(dias="semana")))
                previsao_adicionada = True

            elif contem_palavra("amanhã", parte):
                acoes.append(("acao", lambda: tempo.informar_previsao(dias=2)))
                previsao_adicionada = True

            elif contem_palavra("fim de semana", parte):
                dias_ate_sabado = (5 - dia_atual) % 7 or 7
                acoes.append(("acao", lambda: tempo.informar_previsao(dias=1 + dias_ate_sabado)))
                previsao_adicionada = True

            else:
                for nome_dia, indice in dias_semana.items():
                    if nome_dia in parte:
                        dias_para_dia = (indice - dia_atual) % 7 or 7
                        acoes.append(("acao", lambda d=dias_para_dia: tempo.informar_previsao(dias=d + 1)))
                        previsao_adicionada = True
                        break

                if not previsao_adicionada and "daqui a" in parte and "dias" in parte:
                    match = re.search(r"daqui a (\d+) dias?", parte)
                    if match:
                        dias_futuros = int(match.group(1)) + 1
                        acoes.append(("acao", lambda d=dias_futuros: tempo.informar_previsao(dias=d)))
                        previsao_adicionada = True

            if not previsao_adicionada:
                acoes.append(("acao", tempo.informar_previsao))
            continue

        if contem_qualquer_palavra(palavras_ligar, parte) and contem_qualquer_palavra(palavras_luz, parte):
            acoes.append(("falar", "Ligando a luz."))
            acoes.append(("print", "🔦 Luz ligada."))
            acoes.append(("acao", luz.ligar))
            reconheceu = True
            continue

        if contem_qualquer_palavra(palavras_desligar, parte) and contem_qualquer_palavra(palavras_luz, parte):
            acoes.append(("falar", "Desligando a luz."))
            acoes.append(("print", "🔦 Luz desligada."))
            acoes.append(("acao", luz.desligar))
            reconheceu = True
            continue

        if parte == "ligar":
            acoes.append(("falar", "Ligar o que exatamente?"))
            estado_pendente = "esperando_objeto_para_ligar"
            reconheceu = True
            continue

        if parte == "desligar":
            acoes.append(("falar", "Desligar o que exatamente?"))
            estado_pendente = "esperando_objeto_para_desligar"
            reconheceu = True
            continue

        if contem_qualquer_palavra(palavras_hora, parte) and not falou_hora:
            hora_atual = datetime.now().strftime("%H:%M")
            acoes.append(("falar", f"Agora são {hora_atual}"))
            acoes.append(("print", f"🕒 Agora são {hora_atual}"))
            reconheceu = True
            falou_hora = True
            continue

        if contem_palavra("amanhã", parte) and not falou_data:
            data_amanha = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
            acoes.append(("falar", f"Amanhã será dia {data_amanha}"))
            acoes.append(("print", f"🗓 Amanhã será dia {data_amanha}"))
            reconheceu = True
            falou_data = True
            continue

        if contem_palavra("ontem", parte) and not falou_data:
            data_ontem = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            acoes.append(("falar", f"Ontem foi dia {data_ontem}"))
            acoes.append(("print", f"🗓 Ontem foi dia {data_ontem}"))
            reconheceu = True
            falou_data = True
            continue

        if contem_qualquer_palavra(palavras_data_hoje, parte) and not falou_data:
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            acoes.append(("falar", f"Hoje é {data_hoje}"))
            acoes.append(("print", f"🗓 Hoje é {data_hoje}"))
            reconheceu = True
            falou_data = True
            continue

        if contem_qualquer_palavra(palavras_data_geral, parte) and not falou_data:
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            acoes.append(("falar", f"A data de hoje é {data_hoje}"))
            acoes.append(("print", f"🗓 A data de hoje é {data_hoje}"))
            reconheceu = True
            falou_data = True
            continue

        # Se não reconheceu nenhum comando, pergunte à IA
        if not reconheceu and len(parte) > 3:
            resposta_ia = responder_pergunta(parte)
            ultima_resposta_ia = resposta_ia  # salva última resposta
            acoes.append(("falar", resposta_ia))
            acoes.append(("print", f"🤖 {resposta_ia}"))
            reconheceu = True
            continue

        if parte == "sair":
            falar("Até logo!")
            exit()

    for tipo, valor in acoes:
        if tipo == "falar":
            falar(valor)
        elif tipo == "print":
            print(valor)
        elif tipo == "acao":
            valor()

    if not reconheceu:
        falar("Desculpe, não entendi o que você disse.")
        print("❓ Comando não reconhecido.")
