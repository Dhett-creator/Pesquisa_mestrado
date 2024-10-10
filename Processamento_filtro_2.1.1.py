"""
Esse script realiza o processamento e a filtragem dos dados para diferentes 
concentrações da mesma amostra
"""

import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt


# Função para criar o filtro passa-baixo
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


# Função para aplicar o filtro
def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# Parâmetros do filtro
cutoff_frequency = 55.8  # Frequência de corte do filtro (em Hz)
sampling_rate = 1 / 0.0032  # Taxa de amostragem dos dados (em Hz)
filter_order = 2  # Ordem do filtro

# Define o número máximo de linhas que serão lidas de cada arquivo.csv
max_linhas = 125000

# Lista com os caminhos dos 3 arquivos a serem processados
caminhos_arquivos = [
    "Dados/APD/xx-07-2024/amostra1_1.50/T0001CH4.CSV",
    "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0069CH4.CSV",
    "Dados/APD/xx-07-2024/amostra1_1.70/T0029CH4.CSV",
]

# Processamento de múltiplos arquivos (apenas 3)
for idx, caminho_csv in enumerate(caminhos_arquivos, start=1):
    # Lista para armazenar os dados que estão na 2ª coluna do arquivo de origem
    dados_col2 = []

    # Abre o arquivo de origem em modo de leitura
    with open(caminho_csv, "r") as arquivo:
        leitor_csv = csv.reader(arquivo)

        # Pula as primeiras 16 linhas do arquivo. Essas linhas possuem dados que podem ser descartados
        for _ in range(16):
            next(leitor_csv)

        linhas_lidas = 0
        # Itera sobre as linhas restantes do arquivo
        for linha in leitor_csv:
            # Verifica se a linha não está vazia
            if linha:
                # Adiciona o segundo valor de cada linha à lista "dados_col2"
                dados_col2.append(linha[1])

            # Para o loop quando o número máximo de linhas estabelecido for atingido
            linhas_lidas += 1
            if linhas_lidas >= max_linhas:
                break

    # Define o caminho para a pasta "dados_processados"
    caminho_pasta = "dados_processados"

    # Verifica se a pasta "dados_processados" não existe e a cria se a mesma não existir
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

    # Define o caminho completo para os arquivos .txt dentro da pasta "dados_processados"
    caminho_arquivo_originais = os.path.join(
        caminho_pasta, f"dados_originais_C{idx}.txt"
    )
    caminho_arquivo_filtrados = os.path.join(
        caminho_pasta, f"dados_filtrados_C{idx}.txt"
    )

    # Define o intervalo de tempo em segundos para escrita no arquivo.txt
    intervalo_tempo = 0.0032
    tempo_atual = 0

    # Escreve os dados originais no arquivo .txt
    with open(caminho_arquivo_originais, "w") as arquivo_saida:
        for valor in dados_col2:
            arquivo_saida.write(f"{valor},{tempo_atual:.4f}\n")
            tempo_atual += intervalo_tempo

    # Leitura do arquivo.txt processado
    data = np.loadtxt(caminho_arquivo_originais, delimiter=",")

    # Separa as colunas em variáveis separadas
    dados = data[:, 0]  # Primeira coluna
    tempo = data[:, 1]  # Segunda coluna

    # Aplicar o filtro passa-baixo
    filtered_data = lowpass_filter(dados, cutoff_frequency, sampling_rate, filter_order)

    # Escreve os dados filtrados no arquivo .txt
    tempo_atual = 0
    with open(caminho_arquivo_filtrados, "w") as arquivo_saida:
        for valor in filtered_data:
            arquivo_saida.write(f"{valor},{tempo_atual:.4f}\n")
            tempo_atual += intervalo_tempo
