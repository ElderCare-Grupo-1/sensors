from sensor import Sensor
import random

class LDR(Sensor):
    def __init__(self, localizacao):
        super().__init__("LDR", localizacao)
        self.luminosidade = 0.5  # Valor inicial

    def ler_dados(self, quantidade=1):
        if not self.ativo:
            return None
        
        resultados = []
        for _ in range(quantidade):
            self.luminosidade = max(0, min(1, random.uniform(-0.1, 0.1) + self.luminosidade))
            resultados.append({
                "value": round(self.luminosidade, 2), 
                "localizacao": self.localizacao
            })
        
        return resultados if quantidade > 1 else resultados[0]