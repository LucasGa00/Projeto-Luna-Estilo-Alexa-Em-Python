import threading
import time
from voz import falar

cronometro_ativo = False
tempo_restante = 0
cronometro_thread = None

def iniciar_cronometro(segundos):
    global cronometro_ativo, tempo_restante, cronometro_thread

    cronometro_ativo = True
    tempo_restante = segundos

    cronometro_thread = threading.Thread(target=contar)
    cronometro_thread.start()

    minutos = segundos // 60
    seg_restantes = segundos % 60

    if minutos > 0 and seg_restantes > 0:
        falar(f"Cronômetro iniciado por {minutos} minutos e {seg_restantes} segundos.")
    elif minutos > 0:
        falar(f"Cronômetro iniciado por {minutos} minutos.")
    elif seg_restantes > 0:
        falar(f"Cronômetro iniciado por {seg_restantes} segundos.")

def contar():
    global cronometro_ativo, tempo_restante
    while tempo_restante > 0 and cronometro_ativo:
        time.sleep(1)
        tempo_restante -= 1

    if cronometro_ativo:
        falar("Tempo esgotado!")
    cronometro_ativo = False

def parar_cronometro():
    global cronometro_ativo
    if cronometro_ativo:
        cronometro_ativo = False
        falar("Cronômetro parado.")
    else:
        falar("Nenhum cronômetro está ativo no momento.")

def verificar_tempo():
    global tempo_restante
    if cronometro_ativo:
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        falar(f"Faltam {minutos} minutos e {segundos} segundos.")
    else:
        falar("Não há um cronômetro em andamento.")
