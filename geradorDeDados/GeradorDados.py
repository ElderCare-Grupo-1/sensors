from MFRC522 import Mfrc522
from LDR import LDR
from sensor_lm35 import LM35
from MQ7 import MQ7
from MAX30102 import SPO2Sensor
from HRS3300 import HRS3300
import time
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from datetime import datetime
import csv

class GerenciadorSensores:
    def __init__(self):
        self.localidades = {
            "Cozinha": {
                "rfid": Mfrc522("Cozinha"),
                "sensores": [LDR("Cozinha"), LM35("Cozinha"), MQ7("Cozinha")],
                "ativo": False
            },
            "Sala": {
                "rfid": Mfrc522("Sala"),
                "sensores": [LDR("Sala"), LM35("Sala")],
                "ativo": False
            },
            "Quarto": {
                "rfid": Mfrc522("Quarto"),
                "sensores": [LDR("Quarto"), LM35("Quarto")],
                "ativo": False
            },
            "Garagem": {
                "rfid": Mfrc522("Garagem"),
                "sensores": [MQ7("Garagem")],  # Sensor de CO obrigatório
                "ativo": False
            },
            "Banheiro": {
                "rfid": Mfrc522("Banheiro"),
                "sensores": [MQ7("Banheiro")],  # Sensor de CO obrigatório
                "ativo": False
            }
        }
        
        # Sensores independentes de localização
        self.sensores_globais = [
            SPO2Sensor(),
            HRS3300()
        ]

        self.riscos = {
            "Cozinha": {"total": 0, "motivos": defaultdict(int), "duracao": 0},
            "Sala": {"total": 0, "motivos": defaultdict(int), "duracao": 0},
            "Quarto": {"total": 0, "motivos": defaultdict(int), "duracao": 0},
            "Garagem": {"total": 0, "motivos": defaultdict(int), "duracao": 0},
            "Banheiro": {"total": 0, "motivos": defaultdict(int), "duracao": 0}
        }
        
        self.visitas = defaultdict(int)
        self.ultima_ativacao = {}
        self.limites_risco = {
            "Luminosidade": 30,       # Em lux
            "Temperatura": 28,        # Em °C
            "CO (ppm)": 50           # Partes por milhão
        }
        
        # Dados históricos para os gráficos
        self.dados_historicos = defaultdict(lambda: defaultdict(list))
        self.timestamps = defaultdict(list)
        
        # Ativa todos os sensores RFID inicialmente
        for local in self.localidades.values():
            local["rfid"].ativar()

    def iniciar(self):
        print("Sistema iniciado. Detectando tags RFID automaticamente...")
        print("Cômodos disponíveis:", ", ".join(self.localidades.keys()))
        
        try:
            while True:
                for localizacao, local in self.localidades.items():
                    rfid = local["rfid"]
                    dados_rfid = rfid.ler_dados()
                    
                    if dados_rfid and not local["ativo"]:
                        print(f"\nTag {dados_rfid['tag']} detectada em {localizacao}!")
                        local["ativo"] = True
                        for sensor in local["sensores"]:
                            sensor.ativar()
                        dados = self._ler_dados_sensores(localizacao)
                        self._avaliar_risco(localizacao, dados)
                    elif local["ativo"]:
                        dados = self._ler_dados_sensores(localizacao)
                        risco = self._avaliar_risco(localizacao, dados)
                        if risco:
                            print(f"ALERTA: Condição de risco detectada em {localizacao}!")
                        self._armazenar_dados(localizacao)
                        self.visitas[localizacao] += 1
                
                # Processa sensores globais
                self._ler_dados_sensores_globais()
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nFinalizando sistema...")
            self._gerar_grafico_localizacaos()

    def _avaliar_risco(self, localizacao, dados_sensores):
        if not dados_sensores:  # Se não houver dados, não há risco
            return False
            
        risco_detectado = False
        motivos = []
        
        for sensor_type, dados in dados_sensores:
            if sensor_type == LDR and "luminosidade" in dados and dados["luminosidade"] < self.limites_risco["Luminosidade"]:
                motivos.append("Luminosidade Baixa")
                risco_detectado = True
                
            elif sensor_type == LM35 and "temperatura" in dados and dados["temperatura"] > self.limites_risco["Temperatura"]:
                motivos.append("Temperatura Alta")
                risco_detectado = True
                
            elif sensor_type == MQ7 and "co_ppm" in dados and dados["co_ppm"] > self.limites_risco["CO (ppm)"]:
                motivos.append("Nível de CO Elevado")
                risco_detectado = True
        
        if risco_detectado:
            self.riscos[localizacao]["total"] += 1
            for motivo in motivos:
                self.riscos[localizacao]["motivos"][motivo] += 1
            
            # Calcula tempo de permanência em risco
            if localizacao in self.ultima_ativacao:
                tempo_risco = time.time() - self.ultima_ativacao[localizacao]
                self.riscos[localizacao]["duracao"] += tempo_risco
            else:
                self.ultima_ativacao[localizacao] = time.time()
        
        return risco_detectado

    def _armazenar_dados(self, localizacao):
        timestamp = time.time()
        self.timestamps[localizacao].append(timestamp)
        
        local = self.localidades[localizacao]
        for sensor in local["sensores"]:
            dados = sensor.ler_dados()
            if dados:
                if isinstance(sensor, LDR):
                    # Para o LDR, precisamos calcular a resistência e luminosidade
                    voltSaida = dados  # Assumindo que LDR.ler_dados() retorna a tensão diretamente
                    resistLDR = LDR.resistencia_ldr(voltSaida)
                    luz = LDR.luz_aproximada(resistLDR)
                    self.dados_historicos[localizacao]["Luminosidade"].append(luz)
                elif isinstance(sensor, LM35):
                    self.dados_historicos[localizacao]["Temperatura"].append(dados["temperatura"])
                elif isinstance(sensor, MQ7):
                    # Usando a chave correta 'co_ppm' conforme a implementação do MQ7
                    self.dados_historicos[localizacao]["CO (ppm)"].append(dados["co_ppm"])

    def _ler_dados_sensores(self, localizacao):
        local = self.localidades[localizacao]
        if not local["ativo"]:
            return []
            
        print(f"\n--- Dados em {localizacao} ---")
        dados_sensores = []
        for sensor in local["sensores"]:
            dados = sensor.ler_dados()
            if dados:
                print(f"{sensor.nome}: {dados}")
                dados_sensores.append((type(sensor), dados))
        print("----------------------------")
        return dados_sensores

    def _ler_dados_sensores_globais(self):
        print("\n--- Dados Globais ---")
        for sensor in self.sensores_globais:
            dados = sensor.ler_dados()
            if dados:
                print(f"{sensor.nome}: {dados}")
        print("---------------------")

    def _gerar_grafico_localizacao(self):

        self._gerar_csv_ocorrencias_localizacao()

        locais = list(self.riscos.keys())
        contagem_risco = [v["total"] for v in self.riscos.values()]
        
        plt.figure(figsize=(10, 6))
        
        bars = plt.bar(locais, contagem_risco, color='darkred')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.title('Quantidade de Ocorrências de Risco por Cômodo', pad=20)
        plt.xlabel('Cômodos')
        plt.ylabel('Número de Ocorrências')
        plt.xticks(rotation=45)  
        
        plt.tight_layout()
        
        plt.show()


    def _gerar_csv_ocorrencias_localizacao(self):
        """Gera um arquivo CSV com a contagem de ocorrências por cômodo"""
        # Nome do arquivo com timestamp para evitar sobrescrita
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"ocorrencias_por_comodo_{timestamp}.csv"
        
        # Cabeçalho do CSV
        cabecalho = ["Cômodo", "Ocorrências de Risco", "Tempo em Risco (s)"]
        
        # Dados para escrever no CSV
        dados = []
        for comodo, info in self.riscos.items():
            dados.append([
                comodo, 
                info["total"],
                round(info["duracao"], 2)  # Arredonda para 2 casas decimais
            ])
        
        # Escreve no arquivo CSV
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)
            escritor.writerows(dados)
        
        print(f"\nArquivo CSV gerado com sucesso: {nome_arquivo}")

if __name__ == "__main__":
    gerenciador = GerenciadorSensores()
    gerenciador.iniciar()