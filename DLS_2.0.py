import math
import os
import matplotlib.pyplot as plt
import numpy as np

# Leitura do arquivo.txt
dados_leitura = np.loadtxt("dados_processados/dados_filtrados_M8.txt", delimiter=",")

col1 = dados_leitura[:, 0].astype(float).tolist()  # Dados de intensidade luminosa
col2 = dados_leitura[:, 1].astype(float).tolist()  # Dados de tempo


# Função para contar picos em uma lista de dados
def contar_picos(dados):
    picos = 0
    for i in range(1, len(dados) - 1):
        if dados[i] > dados[i - 1] and dados[i] > dados[i + 1]:
            picos += 1
    return picos


# Intervalo de tempo entre as medições
intervalo_tempo = col2[1] - col2[0]

# Listas para armazenar o número de picos e a densidade de picos
num_picos_lista = []
densidade_picos_lista = []
tempo_intervalo_lista = []

# Contagem de picos progressiva
for num_linhas in range(500, len(col1), 10):
    dados_parciais = col1[:num_linhas]
    num_picos = contar_picos(dados_parciais)
    densidade_picos = num_picos / (intervalo_tempo * num_linhas)
    num_picos_lista.append(num_picos)
    densidade_picos_lista.append(densidade_picos)
    tempo_intervalo_lista.append(num_linhas * intervalo_tempo)

# Calcular diâmetro das partículas
kb = 1.380649 * 10 ** (-23)  # Constante de Boltzmann (J/k)
temp = 22 + 273.15  # Temperatura em Kelvin
n = 1.362  # Índice de refração do solvente (álcool)
eta = 0.0012  # Coeficiente de viscosidade do solvente (N*s/m²)
lamb = 632 * 10 ** (-9)  # Comprimento de onda do laser (em metros)
teta = math.radians(
    20
)  # Ângulo do sensor em relação ao feixe do laser (convertido para radianos)

q = (4 * math.pi * n / lamb) * (math.sin(teta / 2))  # Vetor de espalhamento

list_dnm = []
for rho in densidade_picos_lista:
    if rho != 0:
        dm = (
            ((kb * temp) / (3 * math.pi * eta))
            * (q**2)
            * (math.sqrt(6) / (2 * math.pi * rho))
        )
        dnm = dm * (1 * 10**9)  # Converte o diâmetro para nanômetros
        list_dnm.append(dnm)

# Define o caminho para a pasta "arquivos_gerados"
caminho_pasta = "arquivos_gerados"
if not os.path.exists(caminho_pasta):
    os.makedirs(caminho_pasta)

# Escrever os dados em arquivos
with open(
    os.path.join(caminho_pasta, "num_picos_por_tempo.txt"), "w"
) as arquivo_num_picos:
    arquivo_num_picos.write("Numero de Picos,Tempo (s)\n")
    for num_picos, tempo_intervalo in zip(num_picos_lista, tempo_intervalo_lista):
        arquivo_num_picos.write(f"{num_picos},{tempo_intervalo:.4f}\n")

with open(
    os.path.join(caminho_pasta, "densid_picos_por_tempo.txt"), "w"
) as arquivo_densidade_picos:
    arquivo_densidade_picos.write("Densidade de Picos,Tempo (s)\n")
    for densidade_picos, tempo_intervalo in zip(
        densidade_picos_lista, tempo_intervalo_lista
    ):
        arquivo_densidade_picos.write(f"{densidade_picos},{tempo_intervalo:.4f}\n")

with open(
    os.path.join(caminho_pasta, "diametro_por_tempo.txt"), "w"
) as arquivo_diametro_por_tempo:
    arquivo_diametro_por_tempo.write("Diâmetro (nm),Tempo (s)\n")
    for diam, tempo in zip(list_dnm, tempo_intervalo_lista):
        arquivo_diametro_por_tempo.write(f"{diam:.2f},{tempo:.4f}\n")

# Preparando para plotagem
densidade_picos_coly = []
lista_diam_coly = []
tempo_intervalo_colx = []

with open("arquivos_gerados/densid_picos_por_tempo.txt", "r") as arquivo:
    next(arquivo)
    for linha in arquivo:
        valores = linha.strip().split(",")
        densidade_picos_coly.append(float(valores[0]))
        tempo_intervalo_colx.append(float(valores[1]))

with open("arquivos_gerados/diametro_por_tempo.txt", "r") as arquivo:
    next(arquivo)
    for linha in arquivo:
        valores = linha.strip().split(",")
        lista_diam_coly.append(float(valores[0]))

# Configurações de plotagem
plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]

tam_font = 24

# Densidade média de máximos
dens_media = np.mean(densidade_picos_coly[7765:])
dens_media_str = f"{dens_media:.2f}".replace(".", ",")

# Diâmetro médio
diam_final = np.mean(lista_diam_coly[7765:])
diam_final_str = f"{diam_final:.2f}".replace(".", ",")

# Criar subplots lado a lado
fig, axs = plt.subplots(1, 2, figsize=(25, 8))  # 1 linha, 2 colunas

# Plotando o gráfico de densidade de picos no primeiro eixo
axs[0].plot(
    tempo_intervalo_colx, densidade_picos_coly, label="Valores da densidade de máximos"
)
axs[0].set_xlabel("Tempo (s)", fontsize=tam_font)
axs[0].set_ylabel(r"Densidade de máximos ($s^{-1}$)", fontsize=tam_font)
axs[0].tick_params(axis="both", which="major", labelsize=tam_font)
axs[0].legend(
    [rf"M08; $\langle \rho \rangle$ = {dens_media_str} " r"$s^{-1}$"], fontsize=tam_font
)
axs[0].grid(True)

# Adicionar a identificação 'a)' ao primeiro gráfico
axs[0].annotate(
    "(a)",
    xy=(0.01, 0.95),
    xycoords="axes fraction",
    fontsize=tam_font,
    fontweight="bold",
)

# Plotando o gráfico de diâmetros no segundo eixo
axs[1].plot(tempo_intervalo_colx, lista_diam_coly, label="Valores de Diâmetros")
axs[1].set_xlabel("Tempo (s)", fontsize=tam_font)
axs[1].set_ylabel("Diâmetro hidrodinâmico (nm)", fontsize=tam_font)
axs[1].tick_params(axis="both", which="major", labelsize=tam_font)
axs[1].legend([rf"M08; $\langle d_h \rangle$ = {diam_final_str} nm"], fontsize=tam_font)
axs[1].grid(True)

# Adicionar a identificação 'b)' ao segundo gráfico
axs[1].annotate(
    "(b)",
    xy=(0.01, 0.95),
    xycoords="axes fraction",
    fontsize=tam_font,
    fontweight="bold",
)

# Ajustar espaçamento entre os subplots
plt.tight_layout()

# Salvar figura
plt.savefig("graficos/graficos_densidade_e_diametro.pdf", bbox_inches="tight")
# plt.show()
