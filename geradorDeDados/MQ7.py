import random
import time
import csv
from sensor import Sensor
from datetime import datetime

class MQ7(Sensor):
    def __init__(self, localizacao):
        super().__init__("MQ7", localizacao)
        self.valor_atual = random.uniform(0, 10)
        self.sensor_id = 203  # ID específico para MQ7

    def _simular_leitura(self, chance_evento_raro=0.0001):
        evento_raro = random.random() < chance_evento_raro

        if evento_raro:
            novo_valor = random.uniform(300, 2000)
        else:
            if self.valor_atual > 300:
                variacao_percentual = random.uniform(-10, -3)
            else:
                variacao_percentual = random.uniform(-2, 2)

            novo_valor = self.valor_atual * (1 + variacao_percentual / 100)
            novo_valor = max(3, min(novo_valor, 2000))

        self.valor_atual = novo_valor
        return novo_valor, evento_raro

    def ler_dados(self):
        if not self.ativo:
            return None

        valor, evento_raro = self._simular_leitura()

        if valor <= 9:
            estado = "Seguro"
        elif 10 <= valor <= 50:
            estado = "Exposição Leve"
        elif 51 <= valor <= 150:
            estado = "Exposição Moderada"
        elif 151 <= valor <= 400:
            estado = "Exposição Severa"
        else:
            estado = "Emergência Médica"

        return {
            "timestamp": datetime.now().isoformat(),
            "co_ppm": round(valor, 2),
            "evento_raro": evento_raro,
            "localizacao": self.localizacao,
            "sensor_id": self.sensor_id,
            "estado": estado
        }

    def capturar_serie(self, quantidade, chance_evento_raro=0.001):
        return [round(self._simular_leitura(chance_evento_raro)[0], 2) 
                for _ in range(quantidade)]


if __name__ == "__main__":
    sensor = MQ7("Laboratório Central")
    sensor.ativar()
    intervalo_em_segundos = 60  
    arquivo_csv = "dados_mq7.csv"
    dados = []

    print("Iniciando geração contínua de dados do sensor MQ7...\n")
    
    while True:
        dado = sensor.ler_dados()
        if dado:
            dados.append(dado)
            print(f"[{dado['timestamp']}] Valor: {dado['co_ppm']} ppm | Estado: {dado['estado']}")

        if len(dados) >= intervalo_em_segundos:
            with open(arquivo_csv, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=dado.keys())
                writer.writeheader()
                writer.writerows(dados)
            print(f"💾 CSV salvo com {len(dados)} entradas em '{arquivo_csv}'.\n")
            dados = []

        time.sleep(1)

