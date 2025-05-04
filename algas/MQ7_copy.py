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

    def simular_incendio(self, duracao_minutos=5):
        """Simula um incêndio, onde o CO sobe rapidamente até 2000 ppm."""
        resultados = []
        tempo_segundos = 0
        valor = 15

        while tempo_segundos < duracao_minutos * 60:
            if valor < 200:
                valor = random.uniform(200, 500)
            elif valor < 1000:
                valor = random.uniform(1000, 2000)
            else:
                valor = 2000

            resultados.append({"tempo": tempo_segundos, "value": round(valor, 2)})
            tempo_segundos += 90

        return resultados

    def simular_fogao_mal_regulado(self, duracao_minutos=20):
        """Simula uma combustão incompleta, aumentando lentamente de 100 a 400 ppm."""
        resultados = []
        tempo_segundos = 0
        valor = 15

        while tempo_segundos < duracao_minutos * 60:
            if valor < 100:
                valor += random.uniform(5, 20)
            else:
                valor = min(valor + random.uniform(10, 30), 400)

            resultados.append({"tempo": tempo_segundos, "value": round(valor, 2)})
            tempo_segundos += 90

        return resultados

    def simular_queimadores_pouca_ventilacao(self, duracao_minutos=10):
        """Simula vários queimadores acesos com pouca ventilação, indo de 400 a 800 ppm."""
        resultados = []
        tempo_segundos = 0
        valor = 15

        while tempo_segundos < duracao_minutos * 60:
            if valor < 400:
                valor += random.uniform(30, 50)
            else:
                valor = min(valor + random.uniform(20, 50), 800)

            resultados.append({"tempo": tempo_segundos, "value": round(valor, 2)})
            tempo_segundos += 90

        return resultados

    def simular_sensor_desregulado(self, duracao_minutos=10):
        """Simula um sensor desregulado com valores variando entre 0 e valores altos."""
        resultados = []
        tempo_segundos = 0

        while tempo_segundos < duracao_minutos * 60:
            valor = random.uniform(0, 2000)
            resultados.append({"tempo": tempo_segundos, "value": round(valor, 2)})
            tempo_segundos += 90

        return resultados




import matplotlib.pyplot as plt

# Criando a instância do sensor e simulando os cenários
mq7 = MQ7("Cozinha")
dados_incendio = mq7.simular_incendio()
dados_fogao = mq7.simular_fogao_mal_regulado()
dados_queimadores = mq7.simular_queimadores_pouca_ventilacao()
dados_desregulado = mq7.simular_sensor_desregulado()

# Configurando subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

cenarios = {
    "Incêndio": dados_incendio,
    "Fogão Mal Regulado": dados_fogao,
    "Queimadores + Pouca Ventilação": dados_queimadores,
    "Sensor Desregulado": dados_desregulado
}

# Iterando sobre os cenários e preenchendo os gráficos
for ax, (nome, dados) in zip(axs.flatten(), cenarios.items()):
    tempos = [d["tempo"] for d in dados]
    valores = [d["value"] for d in dados]
    ax.plot(tempos, valores, marker="o", linestyle="-", label=nome)
    ax.set_title(nome)
    ax.set_xlabel("Tempo (segundos)")
    ax.set_ylabel("Concentração de CO (ppm)")
    ax.legend()
    ax.grid(True)

# Ajustando layout
plt.tight_layout()
plt.show()


