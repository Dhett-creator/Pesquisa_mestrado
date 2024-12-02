# Esta versão do script é capaz de processar vários arquivos de uma única vez.

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
cutoff_frequency = 16  # Frequência de corte do filtro (em Hz)
sampling_rate = 1 / 0.0032  # Taxa de amostragem dos dados (em Hz)
filter_order = 4  # Ordem do filtro

# Define o número máximo de linhas que serão lidas de cada arquivo.csv
max_linhas = 125000

# Lista com os caminhos dos arquivos a serem processados
caminhos_arquivos = [
    # ---------------------------- Amostra 1 -----------------------------
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0064CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0065CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0066CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0069CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0070CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0071CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0074CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0075CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0076CH4.CSV",
    # "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0077CH4.CSV",
    # ---------------------------- Amostra 2 -----------------------------
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0059CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0060CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0061CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0064CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0065CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0066CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0067CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0069CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0070CH4.CSV",
    # "Dados/APD/xx-07-2024/amostra2_1.80/T0071CH4.CSV",
    # ---------------------------- Amostra 3 -----------------------------
    "Dados/APD/12-08-2024/amostra3_1.100/T0074CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0075CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0076CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0077CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0078CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0080CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0081CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0082CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0083CH4.CSV",
    "Dados/APD/12-08-2024/amostra3_1.100/T0084CH4.CSV",
]

# Processamento de múltiplos arquivos
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
        caminho_pasta, f"dados_originais_M{idx}.txt"
    )
    caminho_arquivo_filtrados = os.path.join(
        caminho_pasta, f"dados_filtrados_M{idx}.txt"
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
    """
    # Plotar um gráfico da curva original e da curva filtrada
    plt.rcParams["font.family"] = ["DeJavu Serif"]
    plt.rcParams["font.serif"] = ["Times New Roman"]

    tam_font1 = 50

    plt.figure(figsize=(60, 20))
    plt.plot(tempo, dados, label=f"Dados originais M{idx}")
    plt.plot(tempo, filtered_data, label=f"Dados filtrados M{idx}", linewidth=2)
    plt.legend(fontsize=tam_font1)
    plt.xlabel("Tempo (s)", fontsize=tam_font1)
    plt.ylabel("Intensidade", fontsize=tam_font1)
    plt.title(f"Filtro Passa-Baixo M{idx}", fontsize=tam_font1)
    plt.xticks(fontsize=tam_font1)
    plt.yticks(fontsize=tam_font1)
    plt.grid(True)
    plt.savefig(f"graficos/graf_dados_processados_filtrados_M{idx}.pdf", bbox_inches="tight")
    # plt.show()

    # Range do gráfico de recorte
    num_pontos = 600

    tam_font2 = 19

    # Plotar um recorte dos dados originais e dos dados filtrados
    plt.figure(figsize=(12, 6))
    plt.plot(tempo[0:num_pontos], dados[0:num_pontos], label=f"Dados originais M{idx}")
    plt.plot(tempo[0:num_pontos], filtered_data[0:num_pontos], label=f"Dados filtrados M{idx}", linewidth=3)
    plt.legend(fontsize=tam_font2)
    plt.xlabel("Tempo (s)", fontsize=tam_font2)
    plt.ylabel("Intensidade", fontsize=tam_font2)
    # plt.title(f"Recorte - Filtro Passa-Baixo M{idx}", fontsize=tam_font2)
    plt.xticks(fontsize=tam_font2)
    plt.yticks(fontsize=tam_font2)
    plt.grid(True)
    plt.savefig(f"graficos/graf_dados_processados_filtrados_recorte_M{idx}.pdf", bbox_inches="tight")
    # plt.show()
    """
