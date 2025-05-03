import numpy as np
from sensor import Sensor

class SPO2Sensor(Sensor):
    def __init__(self):
        super().__init__("SPO2")
        self.previous_spo2 = 97.0  

    def _generate_dc_r_ir(self):
        dc_r = 500.0
        dc_ir = 600.0
        return dc_r, dc_ir

    def _generate_ac_r_ir(self):
        ac_r = np.random.uniform(5.0, 10.0)
        ac_ir = np.random.uniform(6.0, 12.0)
        return ac_r, ac_ir

    def _calc_spo2(self):
        dc_r, dc_ir = self._generate_dc_r_ir()
        ac_r, ac_ir = self._generate_ac_r_ir()

        if dc_r == 0 or dc_ir == 0 or ac_r == 0 or ac_ir == 0:
            return "Erro: valores DC ou AC são zero, impossível calcular SpO2"

        spo2 = ((ac_r / dc_r) / (ac_ir / dc_ir)) * 100
        return spo2

    def _smooth_spo2(self, current_spo2, alpha=0.1):
        return alpha * current_spo2 + (1 - alpha) * self.previous_spo2

    def ler_dados(self):
        spo2_value = self._calc_spo2()

        if isinstance(spo2_value, (float, int)):
            spo2_value = self._smooth_spo2(spo2_value)
            self.previous_spo2 = spo2_value

            if spo2_value is None:
                status = "Erro na leitura"
            elif spo2_value > 100:
                status = "Possível interferência"
            elif 95 <= spo2_value <= 100:
                status = "Normal"
            elif 90 <= spo2_value < 95:
                status = "Hipóxia Leve"
            elif 85 <= spo2_value < 90:
                status = "Hipóxia Moderada"
            elif 70 <= spo2_value < 85:
                status = "Hipóxia Grave"
            else:
                status = "Crítica ou Sensor desconectado"
                
            return {
                "Oxigenação do sangue": round(spo2_value, 2),
                "unidade": "%",
                "status": status
            }

        return {
            "Oxigenação do sangue": None,
            "unidade": "%",
            "status": "Erro na leitura"
        }