from sensor import Sensor
import random

class Mfrc522(Sensor):
    def __init__(self, localizacao):
        super().__init__("Mfrc522", localizacao)
        self.tags_validas = ["A1B2C3D4", "X5Y6Z7W8", "K9L0M1N2"]

    def ler_dados(self, quantidade=1):
        if not self.ativo:
            return None
        
        resultados = []
        for _ in range(quantidade):
            if random.random() < 0.7:  # 70% de chance de detectar tag
                tag_lida = random.choice(self.tags_validas)
                resultados.append({"tag": tag_lida, "localizacao": self.localizacao})
            else:
                resultados.append(None)
        
        return resultados if quantidade > 1 else resultados[0]