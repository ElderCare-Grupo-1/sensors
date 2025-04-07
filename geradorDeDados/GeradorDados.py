from MFRC522 import Mfrc522
from LDR import LDR
from sensor_lm35 import LM35
from MQ7 import MQ7
from MAX30102 import SPO2Sensor
from HRS3300 import HRS3300
import time

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
        
        # Ativa todos os sensores RFID inicialmente
        for local in self.localidades.values():
            local["rfid"].ativar()

    def iniciar(self):
        print("Sistema iniciado. Detectando tags RFID automaticamente...")
        print("Cômodos disponíveis:", ", ".join(self.localidades.keys()))
        while True:
            # Processa sensores por localização
            for localizacao, local in self.localidades.items():
                rfid = local["rfid"]
                dados_rfid = rfid.ler_dados()
                
                if dados_rfid and not local["ativo"]:
                    print(f"\nTag {dados_rfid['tag']} detectada em {localizacao}!")
                    local["ativo"] = True
                    for sensor in local["sensores"]:
                        sensor.ativar()
                    self._ler_dados_sensores(localizacao)
                elif local["ativo"]:
                    self._ler_dados_sensores(localizacao)
            
            # Processa sensores globais
            self._ler_dados_sensores_globais()
            
            time.sleep(1)

    def _ler_dados_sensores(self, localizacao):
        local = self.localidades[localizacao]
        if not local["ativo"]:
            return
            
        print(f"\n--- Dados em {localizacao} ---")
        for sensor in local["sensores"]:
            dados = sensor.ler_dados()
            if dados:
                print(f"{sensor.nome}: {dados}")
        print("----------------------------")

    def _ler_dados_sensores_globais(self):
        print("\n--- Dados Globais ---")
        for sensor in self.sensores_globais:
            dados = sensor.ler_dados()
            if dados:
                print(f"{sensor.nome}: {dados}")
        print("---------------------")

if __name__ == "__main__":
    gerenciador = GerenciadorSensores()
    gerenciador.iniciar()