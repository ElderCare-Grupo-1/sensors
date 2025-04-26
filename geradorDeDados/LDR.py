from sensor import Sensor
import random
import numpy as np
import matplotlib.pyplot as plt
import time

class LDR(Sensor):
    def __init__(self, localizacao):
        self.luminosidade = 0
        super().__init__("LDR", localizacao)
        self.ativo = True

    @staticmethod
    def resistencia_ldr(voltSaida, resistFixa=10000, voltFonte=5.0):
        return resistFixa * ((voltFonte - voltSaida) / voltSaida)

    @staticmethod
    def luz_aproximada(resistLDR):
        return 100000 / (resistLDR + 1)
    
    def ler_dados(self):
        if not self.ativo:
            return None
        voltSaida = round(random.uniform(0.5, 4.5), 2)
        resistLDR = self.resistencia_ldr(voltSaida)
        luz = self.luz_aproximada(resistLDR)

        if luz > 75:
            print(f"LDR: Luz estimado: {luz:.2f} | Está claro")
        elif luz < 30:
            print(f"LDR: Luz estimado: {luz:.2f} | Está escuro")
        else:
            print(f"LDR: Luz estimado: {luz:.2f} | Iluminação intermediária")

    @staticmethod
    def simular_luz_intermitente():
        voltSaida = []
        for i in range(30):
            if i % 6 < 3:
                v = round(random.uniform(3.5, 4.5), 2)  # luz forte
            else:
                v = round(random.uniform(0.5, 1.0), 2)  # escuro
            voltSaida.append(v)
        return voltSaida

    @staticmethod
    def simular_ambiente_escuro():
        return [round(random.uniform(0.4, 0.8), 2) for _ in range(30)]

    @staticmethod
    def simular_falha_sensor():
        return [random.choice([0, 5, random.uniform(0, 5)]) if i % 5 == 0 else random.uniform(-1, 6) for i in range(30)]

    @staticmethod
    def simular_transicao():
        return np.linspace(4.5, 0.5, 30)

    def plotar(self, voltSaida, titulo):
        tempo = list(range(len(voltSaida)))
        resistencias = [self.resistencia_ldr(v) if v > 0 else float('inf') for v in voltSaida]
        luz = [self.luz_aproximada(r) if r != float('inf') else 0 for r in resistencias]

        plt.figure(figsize=(10, 4))
        plt.plot(tempo, voltSaida, label='Tensão (V)', marker='o')
        plt.plot(tempo, luz, label='Luz estimado', linestyle='--')
        plt.title(titulo)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Valor')
        plt.ylim(0, 100)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --- Executar e exibir todos os cenários com gráfico ---
    def executar_cenarios(self):
        cenarios = [
            ("Luz Intermitente", self.simular_luz_intermitente()),
            ("Ambiente Escuro", self.simular_ambiente_escuro()),
            ("Falha do Sensor", self.simular_falha_sensor()),
            ("Transição Dia/Noite", self.simular_transicao())
        ]
        for nome, dados in cenarios:
            self.plotar(dados, f"Cenário: {nome}")



# ldr = LDR("Sala 01")

# Para ver os gráficos:
# ldr.executar_cenarios()

# Para leitura contínua no terminal:
# ldr.monitorar_continuamente(intervalo=1.0)
