import random
import time
from datetime import datetime
import psutil
import matplotlib.pyplot as plt
import csv
import signal
import sys

class SimuladorBatimentos:
    def __init__(self):
        self.bpm_anterior = random.randint(65, 110)
        self.bpm_pre_erro = self.bpm_anterior
        self.tendencia = random.choice(["neutro", "subindo", "descendo"])
        self.tempo_ultimo_zero = None

        self.dados = []

        plt.ion()
        self.fig, self.ax = plt.subplots(4, 1, figsize=(10, 8))
        self.fig.suptitle("Monitoramento de Batimentos Cardíacos")

    def gerar_bpm(self):
        if random.random() < 0.02:
            novo_bpm = 0
        else:
            if self.tempo_ultimo_zero is not None:
                novo_bpm = max(0, self.bpm_pre_erro + random.randint(-3, 3))
                self.tempo_ultimo_zero = None
            else:
                if self.tendencia == "subindo":
                    variacao = random.randint(1, 5)
                elif self.tendencia == "descendo":
                    variacao = -random.randint(1, 5)
                else:
                    variacao = random.randint(-3, 3)
                novo_bpm = max(0, self.bpm_anterior + variacao)

        agora = datetime.now()

        if novo_bpm == 0:
            if self.tempo_ultimo_zero is None:
                self.tempo_ultimo_zero = agora
                self.bpm_pre_erro = self.bpm_anterior
                status = "Defeito ou Fora de Contato!"
            elif (agora - self.tempo_ultimo_zero).total_seconds() >= 5:
                status = "Manutenção Necessária no Sensor"
            else:
                status = "Defeito ou Fora de Contato!"
        else:
            self.tempo_ultimo_zero = None
            if novo_bpm <= 62 or novo_bpm >= 135:
                status = "Crítico"
            elif 62 < novo_bpm <= 67 or 110 <= novo_bpm < 135:
                status = "Alerta"
            else:
                status = "Bom"

        if novo_bpm != 0:
            if novo_bpm < 57:
                self.tendencia = "subindo"
            elif novo_bpm > 140:
                self.tendencia = "descendo"
            else:
                self.tendencia = random.choice(["neutro", "subindo", "descendo"])

        self.bpm_anterior = novo_bpm
        return agora.strftime("%H:%M:%S"), novo_bpm, status

    def salvar_csv(self):
        with open('dados_batimentos.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Data', 'Hora', 'BPM', 'Status', 'CPU (%)', 'RAM (%)'])
            writer.writerows(self.dados)
        print("\nArquivo CSV salvo como 'dados_batimentos.csv'.")

    def simular(self):
        def sair_graciosamente(sig, frame):
            self.salvar_csv()
            plt.ioff()
            plt.show()
            sys.exit(0)

        signal.signal(signal.SIGINT, sair_graciosamente)

        tempos = []
        bpms_vivo = []
        tempos_alerta = []
        bpms_alerta = []
        tempos_critico = []
        bpms_critico = []
        tempos_defeito = []
        data_defeito = []

        while True:
            hora, bpm, status = self.gerar_bpm()
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            data = datetime.now().strftime("%d-%m-%Y")

            self.dados.append([data, hora, bpm, status, cpu, ram])

            tempos.append(hora)
            bpms_vivo.append(bpm)

            if status == "Alerta":
                tempos_alerta.append(hora)
                bpms_alerta.append(bpm)
            if status == "Crítico":
                tempos_critico.append(hora)
                bpms_critico.append(bpm)
            if status == "Defeito ou Fora de Contato!":
                tempos_defeito.append(hora)
                data_defeito.append(data)


            MAX_PONTOS = 10
            if len(tempos) > MAX_PONTOS:
                tempos = tempos[-MAX_PONTOS:]
                bpms_vivo = bpms_vivo[-MAX_PONTOS:]
                tempos_alerta = tempos_alerta[-MAX_PONTOS:]
                bpms_alerta = bpms_alerta[-MAX_PONTOS:]
                tempos_critico = tempos_critico[-MAX_PONTOS:]
                bpms_critico = bpms_critico[-MAX_PONTOS:]
                tempos_defeito = tempos_defeito[-MAX_PONTOS:]
                data_defeito = data_defeito[-MAX_PONTOS:]

            print(f"[{hora}] BPM: {bpm} | Status: {status} | CPU: {cpu}% | RAM: {ram}%")

            for a in self.ax:
                a.clear()

            self.ax[0].plot(tempos, bpms_vivo, label="Dados ao Vivo", color="blue")
            self.ax[0].set_title("Dados ao Vivo")
            self.ax[0].set_ylabel("BPM")
            self.ax[0].tick_params(axis='x', rotation=45)

            self.ax[1].plot(tempos_alerta, bpms_alerta, label="Dados de Alerta", color="orange")
            self.ax[1].set_title("Dados de Alerta")
            self.ax[1].set_ylabel("BPM")
            self.ax[1].tick_params(axis='x', rotation=45)

            self.ax[2].plot(tempos_critico, bpms_critico, label="Dados Críticos", color="red")
            self.ax[2].set_title("Dados Críticos")
            self.ax[2].set_ylabel("BPM")
            self.ax[2].tick_params(axis='x', rotation=45)

            self.ax[3].scatter(tempos_defeito, data_defeito, color="black", label="Defeitos")
            self.ax[3].set_title("Defeito ou Fora de Contato")
            self.ax[3].set_ylabel("Data")
            self.ax[3].tick_params(axis='x', rotation=45)

            plt.tight_layout()
            plt.pause(0.05)
            time.sleep(1)


if __name__ == "__main__":
    simulador = SimuladorBatimentos()
    simulador.simular()
