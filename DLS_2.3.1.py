"""
Esse script faz a contagem de picos e o cálculo do diâmetro para diferentes 
concentrações da mesma amostra
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import find_peaks

# Listas para armazenar todas as curvas e médias de diâmetros
todas_densidades = []
todas_diametros = []
medias_diametros = []
tempo_intervalo_colx = None

# Definir o intervalo para calcular a média dos diâmetros
intervalo_inicio = 7765
intervalo_fim = None

# Lista de rótulos customizáveis para cada concentração
rotulos_concentracoes = [
    "Concentração = 1:50 mL",
    "Concentração = 1:60 mL",
    "Concentração = 1:70 mL",
]

# Loop para processar os arquivos
for i in tqdm(range(1, 4), desc="Calculando diâmetros"):
    dados_leitura = np.loadtxt(
        f"dados_processados/dados_filtrados_C{i}.txt", delimiter=","
    )
    col1 = dados_leitura[:, 0].astype(float).tolist()
    col2 = dados_leitura[:, 1].astype(float).tolist()

    intervalo_tempo = col2[1] - col2[0]

    num_picos_lista = []
    densidade_picos_lista = []
    tempo_intervalo_lista = []

    for num_linhas in range(500, len(col1), 10):
        dados_parciais = col1[:num_linhas]
        picos, _ = find_peaks(dados_parciais)
        num_picos = len(picos)
        densidade_picos = num_picos / (intervalo_tempo * num_linhas)
        num_picos_lista.append(num_picos)
        densidade_picos_lista.append(densidade_picos)
        tempo_intervalo_lista.append(num_linhas * intervalo_tempo)

    kb = 1.380649e-23  # Constante de Boltzmann (J/K)
    temp = 22 + 273.15  # Temperatura em Kelvin
    n = 1.362  # Índice de refração do solvente (álcool)
    eta = 0.0012  # Viscosidade do solvente (N*s/m²)
    lamb = 632e-9  # Comprimento de onda do laser (m)
    teta = math.radians(20)  # Ângulo em radianos

    q = (4 * math.pi * n / lamb) * (math.sin(teta / 2))

    list_dnm = []
    for rho in densidade_picos_lista:
        if rho != 0:
            dm = (
                ((kb * temp) / (3 * math.pi * eta))
                * (q**2)
                * (3 / (math.pi * math.sqrt(2) * rho))
            )
            dnm = dm * 1e9  # Converter para nanômetros
            list_dnm.append(dnm)

    diam_final = np.mean(list_dnm[intervalo_inicio:intervalo_fim])
    medias_diametros.append(diam_final)

    todas_densidades.append(densidade_picos_lista)
    todas_diametros.append(list_dnm)

    if tempo_intervalo_colx is None:
        tempo_intervalo_colx = tempo_intervalo_lista

plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]
tam_font = 16

plt.figure(figsize=(12, 7))

# Plotar os dados usando os rótulos customizáveis
for j, (diametros, diam_final) in enumerate(
    zip(todas_diametros, medias_diametros), start=1
):
    rotulo_customizado = rotulos_concentracoes[j - 1]  # Usar o rótulo correspondente
    diam_final_str = f"{diam_final:.2f}".replace(".", ",")
    plt.plot(
        tempo_intervalo_colx,
        diametros,
        label=rf"{rotulo_customizado}; $\langle d_h \rangle$ = {diam_final_str} nm",
    )
plt.xlabel("Tempo (s)", fontsize=tam_font)
plt.ylabel("Diâmetro hidrodinâmico (nm)", fontsize=tam_font)
plt.xticks(fontsize=tam_font)
plt.yticks(fontsize=tam_font)
plt.grid(True)

plt.legend(
    fontsize=tam_font,
    loc="upper right",
    ncol=1,  # Legenda em uma única coluna
    bbox_to_anchor=(1, 1),
    title_fontsize=tam_font,
)

# Imprime no terminal os valores que estão na legenda do gráfico
print("\nDiâmetro médio para cada concentração da amostra")
print("-" * 55)

# Imprimir os resultados em uma única coluna
for j, diam_final in enumerate(medias_diametros, start=1):
    rotulo_customizado = rotulos_concentracoes[j - 1]
    diam_final_str = f"{diam_final:.2f}".replace(".", ",")
    print(f"{rotulo_customizado}; ⟨d_h⟩ = {diam_final_str} nm")

print("-" * 55)

# Calcular e exibir a média e o desvio padrão dos valores
media_final = np.mean(medias_diametros)
std_final = np.std(medias_diametros, ddof=1)  # Usando N-1 graus de liberdade
media_final_str = f"{media_final:.2f}".replace(".", ",")
std_final_str = f"{std_final:.2f}".replace(".", ",")

print(f"Média Geral: ⟨d_h⟩ = {media_final_str} ± {std_final_str} nm")
print("-" * 55)

plt.savefig(
    "graficos/graf_diametros_dados_filtrados_diferentes_concent.pdf",
    bbox_inches="tight",
)
