from sensor import Sensor
import random

class LDR(Sensor):
    def __init__(self, localizacao):
        super().__init__("LDR", localizacao)

    def ler_dados(self):
        if not self.ativo:
            return None
        self.luminosidade = max(0, min(1, random.uniform(-0.1, 0.1) + getattr(self, 'luminosidade', 0.5)))
        return {"luminosidade": round(self.luminosidade, 2), "localizacao": self.localizacao}