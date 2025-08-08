import pyttsx3
import speech_recognition as sr

def falar(texto):
    """
    Fala o texto passado como argumento usando o sintetizador de voz
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 235)
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    reconhecedor = sr.Recognizer()
    try:
        with sr.Microphone() as fonte:
            print("Calibrando o ruído ambiente, por favor aguarde...")
            reconhecedor.adjust_for_ambient_noise(fonte, duration=1)  # calibra o ruído ambiente

            reconhecedor.pause_threshold = 1.2  # aguarda até 1.2s de silêncio para considerar fim da fala
            reconhecedor.energy_threshold = 300  # valor padrão, ajuste se necessário
            reconhecedor.dynamic_energy_adjustment_ratio = 1.5

            print("Ouvindo...")
            # Não uso phrase_time_limit para escutar até o fim da fala natural
            audio = reconhecedor.listen(fonte, timeout=10)  # espera até 10s para começar a ouvir

            comando = reconhecedor.recognize_google(audio, language="pt-BR")
            return comando.lower()

    except sr.WaitTimeoutError:
        print("Tempo esgotado esperando fala.")
        return ""
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return ""
    except sr.RequestError:
        print("Erro ao acessar o serviço de voz.")
        return ""
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return ""
