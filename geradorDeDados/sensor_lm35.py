import csv
import time
import random
from sensor import Sensor

class LM35(Sensor):
    def __init__(self, localizacao):
        super().__init__("LM35", localizacao)
        self.temperatura_atual = random.uniform(22, 26) 

    def ler_dados(self):
        if not self.ativo:
            return None

        
        if random.random() < 0.002:  
            temperatura = random.uniform(-55, 150)  
        else:
            variacao = random.uniform(-0.2, 0.2)  
            self.temperatura_atual += variacao
            self.temperatura_atual = max(-55, min(150, self.temperatura_atual)) 
            temperatura = self.temperatura_atual

        return {
            "temperatura": round(temperatura, 2),
            "localizacao": self.localizacao
        }

def verificar_alerta(temperatura):
    """Determina o nível de alerta com base na temperatura"""
    if temperatura < 5:
        nivel = "Crítico"
    elif 5 <= temperatura <= 15:
        nivel = "Alerta"
    elif 16 <= temperatura <= 29:
        nivel = "Bom"
    elif 30 <= temperatura <= 35:
        nivel = "Alerta"
    else: 
        nivel = "Crítico"

    return nivel

def gerar_csv_com_alertas(sensor, nome_arquivo="dados_lm35.csv"):
    """Gera um CSV incluindo alertas de temperatura"""
    with open(nome_arquivo, mode="w", newline="") as arquivo_csv:
        campos = ["timestamp", "temperatura", "alerta"]
        writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
        writer.writeheader()

        sensor.ativo = True  

        for _ in range(60):
            dados = sensor.ler_dados()
            if dados:
                nivel_alerta = verificar_alerta(dados["temperatura"])
                
                writer.writerow({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperatura": dados["temperatura"],
                    "alerta": nivel_alerta
                })

            time.sleep(1)  

if __name__ == "__main__":
    sensor = LM35("Sala")
    gerar_csv_com_alertas(sensor)
