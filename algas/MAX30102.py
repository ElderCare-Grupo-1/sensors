import numpy as np
from sensor import Sensor

class SPO2Sensor(Sensor):
    def __init__(self):
        super().__init__("SPO2")
        self.previous_spo2 = 95.0

    def _generate_dc_r_ir(self):
        sample_rate = 50
        adc_full_scale = np.random.randint(2048, 16384)
        led_r = np.random.randint(1, 50)
        led_ir = np.random.randint(1, 50)
        pulse_width = np.random.randint(50, 400)

        ratio_led_r = led_r / 50 if led_r > 0 else 0
        ratio_led_ir = led_ir / 50 if led_ir > 0 else 0

        dc_r = (ratio_led_r * (adc_full_scale / 2048) * (100 / pulse_width)) * sample_rate
        dc_ir = (ratio_led_ir * (adc_full_scale / 2048) * (100 / pulse_width)) * sample_rate

        return max(dc_r, 0.1), max(dc_ir, 0.1)

    def _generate_ac_r_ir(self):
        sample_rate = 50
        adc_full_scale = np.random.randint(2048, 16384)
        led_r = np.random.randint(1, 50)
        led_ir = np.random.randint(1, 50)
        pulse_width = np.random.randint(50, 400)

        ratio_led_r = led_r / 50 if led_r > 0 else 0
        ratio_led_ir = led_ir / 50 if led_ir > 0 else 0

        ac_r = (ratio_led_r * (adc_full_scale / 2048) * (100 / pulse_width)) * sample_rate * np.random.uniform(0.5, 1.5)
        ac_ir = (ratio_led_ir * (adc_full_scale / 2048) * (100 / pulse_width)) * sample_rate * np.random.uniform(0.5, 1.5)

        return max(ac_r, 0.1), max(ac_ir, 0.1)

    def _calc_spo2(self):
        dc_r, dc_ir = self._generate_dc_r_ir()
        ac_r, ac_ir = self._generate_ac_r_ir()

        if dc_r == 0 or dc_ir == 0 or ac_r == 0 or ac_ir == 0:
            return None

        spo2 = ((ac_r / dc_r) / (ac_ir / dc_ir)) * 100
        return spo2

    def _smooth_spo2(self, current_spo2, alpha=0.1):
        return alpha * current_spo2 + (1 - alpha) * self.previous_spo2

    def ler_dados(self, quantidade=1):
        resultados = []
        for _ in range(quantidade):
            spo2_value = self._calc_spo2()
            
            if isinstance(spo2_value, (float, int)):
                spo2_value = max(0, min(100, spo2_value))
                spo2_value = self._smooth_spo2(spo2_value)
                self.previous_spo2 = spo2_value
                resultados.append({"value": round(spo2_value, 2), "unidade": "%"})
            else:
                resultados.append(None)
        
        return resultados if quantidade > 1 else resultados[0]