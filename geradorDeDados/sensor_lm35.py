from sensor import Sensor
import random

class LM35(Sensor):
    def __init__(self, localizacao):
        super().__init__("LM35", localizacao)

    def ler_dados(self):
        if not self.ativo:
            return None
        
        # Simula temperatura entre 18°C e 30°C (com eventos raros)
        if random.random() < 0.01:  # 1% de chance de evento raro
            temperatura = random.uniform(-55, 150)
        else:
            temperatura = random.uniform(18, 30)
        
        return {
            "temperatura": round(temperatura, 2),
            "localizacao": self.localizacao
        }