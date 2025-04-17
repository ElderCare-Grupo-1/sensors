import random
from sensor import Sensor

class LM35(Sensor):
    def __init__(self, localizacao):
        super().__init__("LM35", localizacao)

    def ler_dados(self, quantidade=1):
        if not self.ativo:
            return None
        
        resultados = []
        for _ in range(quantidade):
            if random.random() < 0.01:  # 1% de chance de evento raro
                temperatura = random.uniform(-55, 150)
            else:
                temperatura = random.uniform(18, 30)
            
            resultados.append({
                "value": round(temperatura, 2),
                "localizacao": self.localizacao
            })
        
        return resultados if quantidade > 1 else resultados[0]