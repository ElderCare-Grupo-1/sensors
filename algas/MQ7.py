import random
from sensor import Sensor

class MQ7(Sensor):
    def __init__(self, localizacao):
        super().__init__("MQ7", localizacao)
        self.valor_atual = random.uniform(0, 10)
        self.sensor_id = 203

    def _simular_leitura(self, chance_evento_raro=0.001):
        evento_raro = random.random() < chance_evento_raro

        if evento_raro:
            return random.uniform(300, 2000), True
        else:
            variacao_percentual = random.uniform(-10, -3) if self.valor_atual > 300 else random.uniform(-2, 2)
            novo_valor = max(20, min(self.valor_atual * (1 + variacao_percentual / 100), 2000))
            return novo_valor, False

    def ler_dados(self, quantidade=1):
        if not self.ativo:
            return None
        
        resultados = []
        for _ in range(quantidade):
            valor, evento_raro = self._simular_leitura()
            self.valor_atual = valor
            resultados.append({
                "value": round(valor, 2),
                "evento_raro": evento_raro,
                "localizacao": self.localizacao,
                "sensor_id": self.sensor_id
            })
        
        return resultados if quantidade > 1 else resultados[0]