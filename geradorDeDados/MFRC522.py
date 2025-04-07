from sensor import Sensor
import random
import time

class Mfrc522(Sensor):
    def __init__(self, localizacao):
        super().__init__("Mfrc522", localizacao)
        self.tags_validas = ["A1B2C3D4", "X5Y6Z7W8", "K9L0M1N2"]  # Tags pré-definidas

    def ler_dados(self):
        if not self.ativo:
            return None
        
        # Simula a detecção automática (70% de chance de detectar uma tag)
        if random.random() < 0.7:
            tag_lida = random.choice(self.tags_validas)
            print(f"Tag {tag_lida} detectada em {self.localizacao}!")
            time.sleep(1)  # Intervalo entre leituras
            return {"tag": tag_lida, "localizacao": self.localizacao}
        else:
            print(f"Busca por tags em {self.localizacao}...")
            time.sleep(1)
            return None