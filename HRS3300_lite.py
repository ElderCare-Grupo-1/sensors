import random
import time
from datetime import datetime, timedelta
import psutil  

class SimuladorBatimentos:
    def __init__(self):
        self.bpm_anterior = random.randint(75, 110)
        self.bpm_pre_erro = self.bpm_anterior
        self.tendencia = random.choice(["neutro", "subindo", "descendo"])
        self.tempo_ultimo_zero = None 

        self.tempo = []
        self.bpm = []
        self.cpu = []
        self.ram = []

    def gerar_bpm(self):
        # 5% de chance de falha do sensor
        if random.random() < 0.05:
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
            if novo_bpm <= 55 or novo_bpm >= 185:
                status = "Crítico"
            elif 55 < novo_bpm <= 60 or 100 <= novo_bpm < 185:
                status = "Alerta"
            else:
                status = "Bom"

        
        if novo_bpm != 0:
            if novo_bpm <= 55:
                self.tendencia = "subindo"
            elif novo_bpm >= 185:
                self.tendencia = "descendo"
            else:
                self.tendencia = random.choice(["neutro", "subindo", "descendo"])

        self.bpm_anterior = novo_bpm
        return agora.strftime("%H:%M:%S"), novo_bpm, status

    def simular(self):
        while True: 
            hora, bpm, status = self.gerar_bpm()
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent

            self.tempo.append(hora)
            self.bpm.append(bpm)
            self.cpu.append(cpu)
            self.ram.append(ram)

            print(f"[{hora}] BPM: {bpm} | Status: {status} | CPU: {cpu}% | RAM: {ram}%")
            time.sleep(1) 

    def simular_em_lote(self, quantidade):
        for _ in range(quantidade):
            hora, bpm, status = self.gerar_bpm()
            cpu = psutil.cpu_percent(interval=None)  
            ram = psutil.virtual_memory().percent

            self.tempo.append(hora)
            self.bpm.append(bpm)
            self.cpu.append(cpu)
            self.ram.append(ram)

            print(f"[{hora}] BPM: {bpm} | Status: {status} | CPU: {cpu}% | RAM: {ram}%")

        print(f"\n >>> Simulação de {quantidade} batimentos finalizada!")


if __name__ == "__main__":
    simulador = SimuladorBatimentos()
    simulador.simular()