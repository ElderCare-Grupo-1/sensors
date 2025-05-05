from sensor import Sensor
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

class LM35(Sensor):
    def __init__(self, localizacao):
        super().__init__("LM35", localizacao)

    def ler_dados(self):
        if not self.ativo:
            return None
        if random.random() < 0.01:
            temperatura = random.uniform(-55, 150)
        else:
            temperatura = random.uniform(16, 29)
        return {
            "temperatura": round(temperatura, 2),
            "localizacao": self.localizacao
        }

def gerar_tempos_em_segundos(quantidade, intervalo_segundos):
    return np.array([i * intervalo_segundos for i in range(quantidade)])

def plotar_temperatura_normal(sensor, quantidade, intervalo):
    dados = [random.uniform(22, 24) for _ in range(quantidade)]
    tempos = gerar_tempos_em_segundos(quantidade, intervalo)

    spl = make_interp_spline(tempos, dados, k=3)
    tempos_novos = np.linspace(tempos[0], tempos[-1], 500)
    dados_suavizados = spl(tempos_novos)

    plt.subplot(2, 2, 1)
    plt.plot(tempos_novos, dados_suavizados, 'g-', label='Temperatura Normal')
    plt.title("Temperatura Normal")
    plt.xlabel("Tempo (s)")
    plt.ylabel("°C")
    plt.ylim(16, 30)
    plt.grid(True)
    plt.legend()

def simular_incendio(sensor, quantidade, intervalo):
    dados = []
    tempos = gerar_tempos_em_segundos(quantidade, intervalo)
    # temperatura começa a aumentar após 67% do tempo total
    ponto_inicio = int(quantidade * 0.67)

    for i in range(quantidade):
        if i < ponto_inicio:
            temp = random.uniform(18, 20)
        else:
            progresso = (i - ponto_inicio) / (quantidade - ponto_inicio)
            temp = 20 + progresso * (150 - 20) + random.uniform(-2, 2)
        dados.append(temp)

    plt.subplot(2, 2, 2)
    plt.plot(tempos, dados, 'k-', label='Temperatura Alta')
    plt.title("Possível Incêndio")
    plt.xlabel("Tempo (s)")
    plt.ylabel("°C")
    plt.ylim(16, 160)
    plt.grid(True)
    plt.legend()

def simular_sensor_desregulado(sensor, quantidade, intervalo):
    dados = [
        random.choice([random.uniform(-100, -20), random.uniform(120, 200)])
        for _ in range(quantidade)
    ]
    tempos = gerar_tempos_em_segundos(quantidade, intervalo)

    plt.subplot(2, 2, 3)
    plt.plot(tempos, dados, 'k-', label='Valores Anômalos')
    plt.title("Sensor Desregulado")
    plt.xlabel("Tempo (s)")
    plt.ylabel("°C")
    plt.grid(True)
    plt.legend()

def simular_temperatura_muito_baixa(sensor, quantidade, intervalo):
    tempos = gerar_tempos_em_segundos(quantidade, intervalo)

    dados = []
    ponto_inicio_queda = int(quantidade * 0.5)
    
    for i in range(quantidade):
        if i < ponto_inicio_queda:
            temperatura = random.uniform(18, 20)  
        else:
            progresso = (i - ponto_inicio_queda) / (quantidade - ponto_inicio_queda)
            temperatura = 19 - progresso * 2 + random.uniform(-1, 1) 

        dados.append(temperatura)

    plt.subplot(2, 2, 4)
    plt.plot(tempos, dados, 'b-', label='Temp. Muito Baixa')
    plt.title("Temperatura Muito Baixa")
    plt.xlabel("Tempo (s)")
    plt.ylabel("°C")
    plt.ylim(10, 30)
    plt.grid(True)
    plt.legend()


if __name__ == "__main__":
    sensor = LM35("Cozinha")
    sensor.ativar()

    quantidade = 125
    intervalo_segundos = 10

    plt.figure(figsize=(12, 8))

    plotar_temperatura_normal(sensor, quantidade, intervalo_segundos)
    simular_incendio(sensor, 120, intervalo_segundos)
    simular_sensor_desregulado(sensor, quantidade, intervalo_segundos)
    simular_temperatura_muito_baixa(sensor, quantidade, intervalo_segundos)

    plt.tight_layout()
    plt.show()
