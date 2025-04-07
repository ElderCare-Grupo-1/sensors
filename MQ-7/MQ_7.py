import random
import json
import matplotlib.pyplot as plt

class Sensor:
    def __init__(self, sensor_id=203):
        self.sensor_id = sensor_id
        self.valor_atual = random.uniform(0, 10)

    def simular_leitura(self, chance_evento_raro):
        evento_raro = random.random() < chance_evento_raro

        if evento_raro:
            novo_valor = random.uniform(300, 2000)
        else:
            if self.valor_atual > 300:
                variacao_percentual = random.uniform(-10, -3)
            else:
                variacao_percentual = random.uniform(-2, 2)

            novo_valor = self.valor_atual * (1 + variacao_percentual / 100)
            novo_valor = max(20, min(novo_valor, 2000))

        self.valor_atual = novo_valor
        return novo_valor, evento_raro

    def capturar_dados(self, quantidade, graph=False, chance_evento_raro=0.001):
        valores = []

        for _ in range(quantidade):
            valor, _ = self.simular_leitura(chance_evento_raro)
            valores.append(round(valor, 2))

        if graph:
            self.plotar_grafico(valores)

        return json.dumps(valores)

    def plotar_grafico(self, valores):
        plt.figure(figsize=(10, 4))
        plt.plot(valores, marker='o', linestyle='-', color='blue')
        plt.title(f'Leituras do Sensor MQ-7 de id:{self.sensor_id}')
        plt.xlabel('Captura')
        plt.ylabel('Valor (ppm)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
