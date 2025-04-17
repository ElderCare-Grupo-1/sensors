import time
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import psutil
import csv
from GeradorDados import GerenciadorSensores 

class GerenciadorSensoresTester:
    def __init__(self, db_config):
        self.db_config = db_config
        self.gerenciador = GerenciadorSensores()
        self.dadosColetados = []
        self.results = []
        
    def collect_sensor_data(self, num_readings):
        self.dadosColetados = self.gerenciador.iniciar(num_readings).copy()
        print("Dados", self.dadosColetados)
        return self.dadosColetados
    
    def _format_reading(self, sensor_name, reading):
        """Formata a leitura para inserção no MySQL"""
        sensor_ids = {
            "HRS3300": 1,
            "SPO2Sensor": 2,
            "LDR": 3,
            "LM35": 4,
            "MQ7": 5,
            "Mfrc522": 6
        }
        
        # Extrai o valor dependendo da estrutura do dado
        if isinstance(reading, dict):
            if "bpm" in reading:  # Sensor de frequência cardíaca
                value = reading["bpm"]
            elif "Oxigeação do sangue" in reading:  # Sensor SPO2
                value = reading["Oxigeação do sangue"]
            elif "luminosidade" in reading:  # Sensor LDR
                value = reading["luminosidade"]
            elif "temperatura" in reading:  # Sensor LM35
                value = reading["temperatura"]
            elif "co_ppm" in reading:  # Sensor MQ7
                value = reading["co_ppm"]
            elif "tag" in reading:  # Sensor RFID
                value = 1 if reading["tag"] else 0  # Binário para RFID
            else:
                value = list(reading.values())[0]  # Pega o primeiro valor
        else:
            value = float(reading) if str(reading).replace('.', '').isdigit() else 0
        
        return (
            round(float(value), 2),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sensor_ids.get(sensor_name, 1)  # Default para ID 1 se não encontrado
        )
    
    def test_performance(self, batch_sizes):
        
        for batch_size in batch_sizes:
            print(f"\n► TESTANDO TAMANHO DE LOTE: {batch_size}")
            
            gen_start = time.time()
            all_data = []
            
            collected = self.collect_sensor_data(batch_size)
            all_data.extend(collected)

            
            gen_time = time.time() - gen_start
            
            # Divide em lotes para inserção
            batches = [all_data[i:i + batch_size] for i in range(0, len(all_data), batch_size)]
            
            # Teste de inserção
            insert_metrics = self._test_insert_performance()
            
            # Armazena resultados
            self.results.append({
                'batch_size': batch_size,
                'total_readings': len(all_data),
                'gen_time': gen_time,
                **insert_metrics,
                'reads_per_sec': len(all_data) / insert_metrics['insert_time'] if insert_metrics['insert_time'] > 0 else 0,
                'gen_rate': len(all_data) / gen_time if gen_time > 0 else 0
            })
            
            self._print_current_results()
            self.dadosColetados = []
        
        # Gera relatórios finais
        self._save_results()
        self._generate_charts()
    
    def get_all_sensors(self):
        sensors = []
        
        # Sensores por localização
        for local in self.gerenciador.localidades.values():
            sensors.extend(local["sensores"])
        
        # Sensores globais
        sensors.extend(self.gerenciador.sensores_globais)
        
        return sensors
    
    def _test_insert_performance(self):
        conn = None
        metrics = {
            'insert_time': 0,
            'cpu_time': 0,
            'memory_used': 0
        }
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Prépara query
            queryDadosSensores = """
            INSERT INTO raw_data (value) 
                VALUES (%s)
            """
            
            # Transforma cada valor float em uma tupla de um elemento
            dados_formatados = [(valor,) for valor in self.dadosColetados]
            
            start_time = time.time()
            start_cpu = time.process_time()
            start_mem = psutil.virtual_memory().used

            cursor.executemany(queryDadosSensores, dados_formatados)
            conn.commit()
            
            metrics['insert_time'] = time.time() - start_time
            metrics['cpu_time'] = time.process_time() - start_cpu
            metrics[''] = (psutil.virtual_memory().used - start_mem) / (1024 * 1024)  # MB

            queryDadosMaquina = """
            INSERT INTO machine_raw_data (value, components_idcomponents)
                VALUES (%s, %s)
            """

            cursor.execute(queryDadosMaquina, (metrics["insert_time"], 4))
            conn.commit()

            cursor.execute(queryDadosMaquina, (metrics['cpu_time'], 5))
            conn.commit()

            cursor.execute(queryDadosMaquina, (metrics['memory_used'], 6))
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Erro MySQL: {err}")
        finally:
            if conn:
                conn.close()
        
        return metrics
    
    def _print_current_results(self):
        last = self.results[-1]
        print("\nRESULTADOS:")
        print(f"  Tamanho do lote: {last['batch_size']}")
        print(f"  Leituras coletadas: {last['total_readings']}")
        print(f"  Tempo coleta: {last['gen_time']:.4f}s ({last['gen_rate']:.2f} leituras/s)")
        print(f"  Tempo inserção: {last['insert_time']:.4f}s ({last['reads_per_sec']:.2f} leituras/s)")
        print(f"  Tempo CPU: {last['cpu_time']:.4f}s")
        print(f"  Memória usada: {last['memory_used']:.2f} MB")
    
    def _save_results(self):
        """Salva resultados em CSV"""
        filename = f"gerenciador_sensores_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Tamanho Lote', 'Total Leituras', 'Tempo Coleta (s)',
                'Taxa Coleta (leituras/s)', 'Tempo Inserção (s)',
                'Taxa Inserção (leituras/s)', 'Tempo CPU (s)', 'Uso Memória (MB)'
            ])
            
            for r in self.results:
                writer.writerow([
                    r['batch_size'], r['total_readings'], r['gen_time'],
                    r['gen_rate'], r['insert_time'], r['reads_per_sec'],
                    r['cpu_time'], r['memory_used']
                ])
        
        print(f"\n✔ Resultados salvos em {filename}")
    
    def _generate_charts(self):
        """Gera gráficos comparativos"""
        plt.figure(figsize=(18, 10))
        
        # Gráfico 1: Tempos de coleta e inserção
        plt.subplot(2, 2, 1)
        batch_sizes = [r['batch_size'] for r in self.results]
        plt.plot(batch_sizes, [r['gen_time'] for r in self.results], 'b-o', label='Coleta')
        plt.plot(batch_sizes, [r['insert_time'] for r in self.results], 'g-s', label='Inserção')
        plt.title('Tempo de Coleta vs Inserção')
        plt.xlabel('Tamanho do Lote')
        plt.ylabel('Tempo (segundos)')
        plt.legend()
        plt.grid(True)
        
        # Gráfico 2: Taxas de processamento
        plt.subplot(2, 2, 2)
        plt.plot(batch_sizes, [r['gen_rate'] for r in self.results], 'b-o', label='Coleta')
        plt.plot(batch_sizes, [r['reads_per_sec'] for r in self.results], 'g-s', label='Inserção')
        plt.title('Taxa de Processamento')
        plt.xlabel('Tamanho do Lote')
        plt.ylabel('Leituras/segundo')
        plt.legend()
        plt.grid(True)
        
        # Gráfico 3: Uso de CPU
        plt.subplot(2, 2, 3)
        plt.plot(batch_sizes, [r['cpu_time'] for r in self.results], 'r-^')
        plt.title('Tempo de CPU')
        plt.xlabel('Tamanho do Lote')
        plt.ylabel('Segundos')
        plt.grid(True)
        
        # Gráfico 4: Uso de Memória
        plt.subplot(2, 2, 4)
        plt.plot(batch_sizes, [r['memory_used'] for r in self.results], 'm-d')
        plt.title('Uso de Memória')
        plt.xlabel('Tamanho do Lote')
        plt.ylabel('MB')
        plt.grid(True)
        
        plt.tight_layout()
        
        # Salva gráficos
        chart_file = f"gerenciador_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(chart_file)
        plt.close()
        print(f"✔ Gráficos salvos em {chart_file}")


if __name__ == "__main__":
    # Configuração do MySQL - ajuste com seus dados
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Nino0911',
        'database': 'elder_care',
        'autocommit': False
    }
    
    tester = GerenciadorSensoresTester(db_config)
    
    batch_sizes = [60, 600, 6000,   ]
    
    # Executa testes
    tester.test_performance(batch_sizes)