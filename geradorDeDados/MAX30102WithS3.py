import numpy as np
import pandas as pd
import boto3
import time
from sensor import Sensor


# 🔐🔧 === Constantes de configuração AWS ===
# AWS_ACCESS_KEY_ID = "ASIA25W5A4K2ITQTK3RB"
# AWS_SECRET_ACCESS_KEY = "fxtA88lDRgum2OvAJwF0tLSiMpC/XmUvCO++4QSq"
# AWS_REGION = "us-east-1"

S3_BUCKET_NAME = "raw-eldercare-elder-care-4"
S3_FILE_PATH = "spo2_dados.csv"

# 📄 Nome do arquivo CSV local
LOCAL_CSV_FILE = "spo2_dados.csv"


# ================= SENSOR ===================
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

        ratio_led_r = led_r / 50
        ratio_led_ir = led_ir / 50

        dc_r = (ratio_led_r * (adc_full_scale / 2048) * (100 / pulse_width)) * sample_rate
        dc_ir = (ratio_led_ir * (adc_full_scale / 2048) * (100 / pulse_width)) * sample_rate

        return max(dc_r, 0.1), max(dc_ir, 0.1)

    def _generate_ac_r_ir(self):
        sample_rate = 50
        adc_full_scale = np.random.randint(2048, 16384)
        led_r = np.random.randint(1, 50)
        led_ir = np.random.randint(1, 50)
        pulse_width = np.random.randint(50, 400)

        ratio_led_r = led_r / 50
        ratio_led_ir = led_ir / 50

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

    def ler_dados(self):
        spo2_value = self._calc_spo2()

        if spo2_value is not None:
            spo2_value = min(max(spo2_value, 0), 100)
            spo2_value = self._smooth_spo2(spo2_value)
            self.previous_spo2 = spo2_value
            return {
                "Oxigenacao_do_sangue": round(spo2_value, 2),
                "Unidade": "%",
                "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
        return None


# ================= CSV ===================
def gerar_csv(sensor: SPO2Sensor, nome_arquivo: str):
    dados = []

    for _ in range(100):
        leitura = sensor.ler_dados()
        if leitura:
            dados.append(leitura)
        time.sleep(0.1)  # Simula intervalo de leitura (100ms)

    df = pd.DataFrame(dados)
    df.to_csv(nome_arquivo, index=False, sep=';')
    print(f"✅ CSV '{nome_arquivo}' gerado com sucesso!")
    return nome_arquivo


# ================= S3 ===================
def upload_para_s3(nome_arquivo: str, bucket: str, caminho_s3: str):
    s3 = boto3.client(
        's3',
    )
    try:
        s3.upload_file(nome_arquivo, bucket, caminho_s3)
        print(f"🚀 Arquivo '{nome_arquivo}' enviado para 's3://{bucket}/{caminho_s3}' com sucesso!")
    except Exception as e:
        print("❌ Erro no upload:", e)


# ================= MAIN ===================
if __name__ == "__main__":
    sensor_spo2 = SPO2Sensor()

    while True:
        gerar_csv(sensor_spo2, LOCAL_CSV_FILE)
        upload_para_s3(LOCAL_CSV_FILE, S3_BUCKET_NAME, S3_FILE_PATH)
        time.sleep(60)
