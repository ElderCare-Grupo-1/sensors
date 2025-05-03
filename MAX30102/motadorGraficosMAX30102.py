import pandas as pd
import matplotlib.pyplot as plt
import math

file_path = r'd:\repos\sensors\geradorDeDados\MAX30102\resultado_oxigenacao.csv'

try:
    data = pd.read_csv(file_path, sep=';')
except FileNotFoundError:
    print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    exit()

data['nomeCenario'] = data['nomeCenario'].str.strip().str.lower()

def gerar_graficos_em_grade(data):
    cenarios = data['nomeCenario'].unique()
    num_cenarios = len(cenarios)

    cols = 3
    rows = math.ceil(num_cenarios / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows), sharex=False)
    axes = axes.flatten()

    for i, cenario in enumerate(cenarios):
        subset = data[data['nomeCenario'] == cenario]

        if subset.empty:
            print(f"Aviso: O cenário '{cenario}' não possui dados.")
            continue

        if subset['dado'].isnull().all():
            print(f"Aviso: O cenário '{cenario}' contém apenas valores nulos.")
            continue

        x_values = range(len(subset))
        axes[i].plot(x_values, subset['dado'].values, label=cenario, color='blue', linewidth=1)
        axes[i].set_title(f'Cenário: {cenario}', fontsize=10)
        axes[i].set_xlabel('Número do Dado', fontsize=8)
        axes[i].set_ylabel('Dado', fontsize=8)
        axes[i].set_xlim(0, len(subset) - 1)
        axes[i].legend(fontsize=8)

    for j in range(num_cenarios, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(pad=2.0, w_pad=1.5, h_pad=4.0)
    plt.savefig('graficos_cenarios_em_grade_compactos.png')
    plt.show()

gerar_graficos_em_grade(data)
