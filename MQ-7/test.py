from MQ_7 import Sensor as mq7

def testar_sensor():
    sensor = mq7(sensor_id=101)
    # Considerando que o Sensor MQ-7 em sua rotina comum realiza a captura a cada 90s, 350.400 registros equivalem a 1 ano de funcionamento ininterrupto do sensor
    resultado_json = sensor.capturar_dados(
        quantidade=350400,
        graph=False,
        chance_evento_raro=0.0001
    )
    print(resultado_json)

if __name__ == "__main__":
    testar_sensor()
