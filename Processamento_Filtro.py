import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt


# Definir a função para criar o filtro passa-baixo
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


# Definir a função para aplicar o filtro
def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# Parâmetros do filtro
cutoff_frequency = 35  # Frequência de corte do filtro (em Hz)
sampling_rate = 1 / 0.0032  # Taxa de amostragem dos dados (em Hz)
filter_order = 2  # Ordem do filtro

# Lista para armazenar os dados que estão na 2ª coluna do arquivo de origem
dados_col2 = []

# Define o número máximo de linhas que serão lidas do arquivo.csv
max_linhas = 125000

# Abre o arquivo de oriigem em modo de leitura
with open(
    "Dados/APD/06-06-2024/120nm concent.60-1 20g temp.22 T0075CH4.CSV", "r"
) as arquivo:
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

# Define o caminho completo para o "arquivo.txt" dentro da pasta "dados_processados"
caminho_arquivo = os.path.join(caminho_pasta, "dados_originais.txt")

# Define o intervalo de tempo em segundos para escrita no arquivo.txt
intervalo_tempo = 0.0032
tempo_atual = 0

# Abre o "arquivo.txt" em modo de escrita dentro da pasta "dados_processados"
with open(caminho_arquivo, "w") as arquivo_saida:
    # Escreve os segundos valores e o tempo correspondente no arquivo de saída
    for valor in dados_col2:
        arquivo_saida.write(f"{valor},{tempo_atual:.4f}\n")
        tempo_atual += intervalo_tempo

# Leitura do arquivo.txt processado
data = np.loadtxt("dados_processados/dados_originais.txt", delimiter=",")

# Separa as colunas em variáveis separadas
dados = data[:, 0]  # Primeira coluna
tempo = data[:, 1]  # Segunda coluna

# Aplicar o filtro passa-baixo
filtered_data = lowpass_filter(dados, cutoff_frequency, sampling_rate, filter_order)

# Abre um "arquivo.txt" em modo de escrita dentro da pasta "dados_processados"
caminho_arquivo = os.path.join(caminho_pasta, "dados_filtrados.txt")
tempo_atual = 0
with open(caminho_arquivo, "w") as arquivo_saida:
    # Escreve os segundos valores e o tempo correspondente no arquivo de saída
    for valor in filtered_data:
        arquivo_saida.write(f"{valor},{tempo_atual:.4f}\n")
        tempo_atual += intervalo_tempo

# Plotar um gráfico da curva original e da curva filtrada
plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]

tam_font1 = 50

plt.figure(figsize=(60, 20))
plt.plot(tempo, dados, label="Dados originais")
plt.plot(tempo, filtered_data, label="Dados filtrados", linewidth=2)
plt.legend(fontsize=tam_font1)
plt.xlabel("Tempo (s)", fontsize=tam_font1)
plt.ylabel("Intensidade", fontsize=tam_font1)
plt.title("Filtro Passa-Baixo", fontsize=tam_font1)
plt.xticks(fontsize=tam_font1)
plt.yticks(fontsize=tam_font1)
plt.grid(True)
plt.savefig("graficos/graf_dados_processados_filtrados.pdf", bbox_inches="tight")
# plt.show(block=False)

# Range do gráfico de recorte
num_pontos = 600

tam_font2 = 19

# Plotar um recorte dos dados originais e dos dados filtrados
plt.figure(figsize=(12, 6))
plt.plot(tempo[0:num_pontos], dados[0:num_pontos], label="Dados originais")
plt.plot(
    tempo[0:num_pontos],
    filtered_data[0:num_pontos],
    label="Dados filtrados",
    linewidth=3,
)
plt.legend(fontsize=tam_font2)
plt.xlabel("Tempo (s)", fontsize=tam_font2)
plt.ylabel("Intensidade", fontsize=tam_font2)
# plt.title("Recorte - Filtro Passa-Baixo", fontsize=tam_font2)
plt.xticks(fontsize=tam_font2)
plt.yticks(fontsize=tam_font2)
plt.grid(True)
plt.savefig(
    "graficos/graf_dados_processados_filtrados_recorte.pdf", bbox_inches="tight"
)
# plt.show()
