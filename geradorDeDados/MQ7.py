import random
from sensor import Sensor

class MQ7(Sensor):
    def __init__(self, localizacao):
        super().__init__("MQ7", localizacao)
        self.valor_atual = random.uniform(0, 10)
        self.sensor_id = 203  # ID específico para MQ7

    def _simular_leitura(self, chance_evento_raro=0.001):
        """Simula a leitura do sensor com chance de eventos raros"""
        evento_raro = random.random() < chance_evento_raro

        if evento_raro:
            novo_valor = random.uniform(300, 2000)
        else:
            if self.valor_atual > 300:
                variacao_percentual = random.uniform(-10, -3)
            else:
                variacao_percentual = random.uniform(-2, 2)

            novo_valor = self.valor_atual * (1 + variacao_percentual / 100)
            novo_valor = max(20, min(novo_valor, 2000))

        self.valor_atual = novo_valor
        return novo_valor, evento_raro

    def ler_dados(self):
        """Retorna os dados no formato padronizado do sistema"""
        if not self.ativo:
            return None
        
        valor, evento_raro = self._simular_leitura()
        return {
            "co_ppm": round(valor, 2),
            "evento_raro": evento_raro,
            "localizacao": self.localizacao,
            "sensor_id": self.sensor_id
        }

    def capturar_serie(self, quantidade, chance_evento_raro=0.001):
        """Captura uma série de leituras (para uso externo)"""
        return [round(self._simular_leitura(chance_evento_raro)[0], 2) 
               for _ in range(quantidade)]