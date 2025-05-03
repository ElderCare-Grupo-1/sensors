import random
import csv
from MAX30102 import SPO2Sensor
import os


class SPO2ScenarioSimulator:
    def __init__(self, scenario: str, quantidade_dados: int):
        self.sensor = SPO2Sensor()
        self.scenario = scenario.lower()
        self.quantidade_dados = quantidade_dados

    def _apply_scenario(self):
        if self.scenario == "normal":
            self.sensor._generate_dc_r_ir = lambda: (600.0, 620.0)
            self.sensor._generate_ac_r_ir = lambda: (9.0, 10.0)
        elif self.scenario == "hipoxia_leve":
            self.sensor._generate_dc_r_ir = lambda: (500.0, 520.0)
            self.sensor._generate_ac_r_ir = lambda: (10.0, 12.0)
        elif self.scenario == "hipoxia_moderada":
            self.sensor._generate_dc_r_ir = lambda: (500.0, 550.0)
            self.sensor._generate_ac_r_ir = lambda: (15.0, 25.0)
        elif self.scenario == "hipoxia_grave":
            self.sensor._generate_dc_r_ir = lambda: (400.0, 600.0)
            self.sensor._generate_ac_r_ir = lambda: (100.0, 300.0)
        elif self.scenario == "sensor_desconectado":
            self.sensor._generate_dc_r_ir = lambda: (0.0, 0.0)
            self.sensor._generate_ac_r_ir = lambda: (0.0, 0.0)
        elif self.scenario == "interferencia":
            self.sensor._generate_dc_r_ir = lambda: (500.0, 500.0)
            self.sensor._generate_ac_r_ir = lambda: (3000.0, 50.0)
        else:
            raise ValueError(f"Cenário '{self.scenario}' não reconhecido.")

    def simular(self):
        self._apply_scenario()
        dados = []
        for _ in range(self.quantidade_dados):
            oxigenacao_sangue = self.sensor.ler_dados()

            status = oxigenacao_sangue["status"]

            dados.append({
                'nomeCenario': self.scenario,
                'oxigenacaoSangue': oxigenacao_sangue["Oxigenação do sangue"],
                'unidade': '%',
                'status': status
            })
        return dados


def salvar_csv(dados, nome_arquivo):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)

    print(f"Salvando arquivo em: {caminho_arquivo}")
    
    # Abrir o arquivo diretamente no modo de escrita para sobrescrever
    with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['nomeCenario', 'dado', 'unidade', 'status'])
        for dado in dados:
            writer.writerow([dado['nomeCenario'], dado['oxigenacaoSangue'], dado['unidade'], dado['status']])

if __name__ == "__main__":
    cenarios = [
        "normal", "hipoxia_leve", "hipoxia_moderada", "hipoxia_grave",
        "sensor_desconectado", "interferencia"
    ]

    quantidade_por_cenario = 600
    random.seed(42)

    todos_dados = []
    for nome in cenarios:
        print(f"\nSimulando cenário: {nome.upper()} com {quantidade_por_cenario} dados")
        sim = SPO2ScenarioSimulator(nome, quantidade_por_cenario)
        resultados = sim.simular()
        todos_dados.extend(resultados)

    salvar_csv(todos_dados, 'resultado_oxigenacao.csv')
    print("Dados salvos no arquivo 'resultado_oxigenacao.csv'.")