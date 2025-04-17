import random
from sensor import Sensor
from datetime import datetime

class HRS3300(Sensor):
    def __init__(self):
        super().__init__("HeartRate")
        self.previous_bpm = random.randint(75, 110)
        self.trend = random.choice(["neutro", "subindo", "descendo"])

    def _generate_heart_rate(self):
        if self.trend == "subindo":
            variation = random.randint(3, 7)
        elif self.trend == "descendo":
            variation = random.randint(-7, -3)
        else:
            variation = random.randint(-5, 5)
        
        bpm = self.previous_bpm + variation
        
        if bpm >= 185:
            self.trend = "descendo"
        elif bpm <= 55:
            self.trend = "subindo"
        elif 95 < bpm < 130:
            self.trend = random.choice(["subindo", "descendo"])
        else:
            self.trend = random.choice(["neutro", "subindo", "descendo"])
        
        return bpm

    def ler_dados(self, quantidade=1):
        resultados = []
        for _ in range(quantidade):
            bpm = self._generate_heart_rate()
            self.previous_bpm = bpm
            
            if bpm < 55 or bpm > 185:
                status = "Crítico"
            elif 95 <= bpm <= 130:
                status = "Alerta"
            else:
                status = "Bom"
            
            resultados.append({
                "value": bpm,
                "status": status,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return resultados if quantidade > 1 else resultados[0]