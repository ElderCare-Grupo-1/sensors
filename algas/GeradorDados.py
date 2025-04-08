from MFRC522 import Mfrc522
from LDR import LDR
from sensor_lm35 import LM35
from MQ7 import MQ7
from MAX30102 import SPO2Sensor
from HRS3300 import HRS3300

class GerenciadorSensores:
    def __init__(self):
        self.localidades = {
            "Cozinha": {
                "rfid": Mfrc522("Cozinha"),
                "sensores": [LDR("Cozinha"), LM35("Cozinha"), MQ7("Cozinha")],
                "ativo": False
            },
            # ... (outras localidades mantêm a mesma estrutura)
        }
        self.sensores_globais = [SPO2Sensor(), HRS3300()]

    def ler_dados_em_quantidade(self, quantidade):
        dados = {}
        
        # Sensores por localização
        for localizacao, local in self.localidades.items():
            if local["ativo"]:
                dados_local = []
                for sensor in local["sensores"]:
                    dados_sensor = sensor.ler_dados(quantidade)
                    dados_local.append({
                        "sensor": sensor.nome,
                        "dados": dados_sensor
                    })
                dados[localizacao] = dados_local
        
        # Sensores globais
        dados_globais = []
        for sensor in self.sensores_globais:
            dados_sensor = sensor.ler_dados(quantidade)
            dados_globais.append({
                "sensor": sensor.nome,
                "dados": dados_sensor
            })
        dados["global"] = dados_globais
        
        return dados

    def ativar_todos(self):
        for local in self.localidades.values():
            local["ativo"] = True
            for sensor in local["sensores"]:
                sensor.ativar()
        return True