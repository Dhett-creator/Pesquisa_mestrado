import math
import os
import matplotlib.pyplot as plt
import numpy as np

# Leitura do arquivo.txt
dados_leitura = np.loadtxt("dados_processados/dados_filtrados.txt", delimiter=",")

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

# Lista para armazenar o tempo correspondente a cada intervalo
tempo_intervalo_lista = []

# Contagem de picos progressiva
for num_linhas in range(500, len(col1), 10):  # Ajustar o range conforme desejado
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
        # O resultado de 'dm' é dado em metros.
        dm = (
            ((kb * temp) / (3 * math.pi * eta))
            * (q**2)
            * (math.sqrt(6) / (2 * math.pi * rho))
        )

        dnm = dm * (1 * 10**9)  # Converte o diâmetro para nanômetros
        list_dnm.append(dnm)

# Define o caminho para a pasta "arquivos_gerados"
caminho_pasta = "arquivos_gerados"
# Verifica se a pasta "arquivos_gerados" já existe. Caso não exista ela será criada
if not os.path.exists(caminho_pasta):
    os.makedirs(caminho_pasta)

# Escrever os dados em "num_picos_por_tempo.txt"
with open(
    os.path.join(caminho_pasta, "num_picos_por_tempo.txt"), "w"
) as arquivo_num_picos:
    arquivo_num_picos.write("Numero de Picos,Tempo (s)\n")
    for num_picos, tempo_intervalo in zip(num_picos_lista, tempo_intervalo_lista):
        arquivo_num_picos.write(f"{num_picos},{tempo_intervalo:.4f}\n")

# Escrever os dados em "densid_picos_por_tempo.txt"
with open(
    os.path.join(caminho_pasta, "densid_picos_por_tempo.txt"), "w"
) as arquivo_densidade_picos:
    arquivo_densidade_picos.write("Densidade de Picos,Tempo (s)\n")
    for densidade_picos, tempo_intervalo in zip(
        densidade_picos_lista, tempo_intervalo_lista
    ):
        arquivo_densidade_picos.write(f"{densidade_picos},{tempo_intervalo:.4f}\n")

# Escrever os diâmetros em função dos intervalos de tempo no arquivo 'diametro_por_tempo.txt'
with open(
    os.path.join(caminho_pasta, "diametro_por_tempo.txt"), "w"
) as arquivo_diametro_por_tempo:
    arquivo_diametro_por_tempo.write("Diâmetro (nm),Tempo (s)\n")
    for diam, tempo in zip(list_dnm, tempo_intervalo_lista):
        arquivo_diametro_por_tempo.write(f"{diam:.2f},{tempo:.4f}\n")

# Listas para armazenar que dados serão usados para plotagem dos gráficos
densidade_picos_coly = []
lista_diam_coly = []
tempo_intervalo_colx = []

# Leitura dos dados do arquivo "densid_picos_por_tempo.txt"
with open("arquivos_gerados/densid_picos_por_tempo.txt", "r") as arquivo:
    # Ignorando o cabeçalho do arquivo
    next(arquivo)

    # Iterando sobre as linhas do arquivo
    for linha in arquivo:
        # Separando os valores da linha e os adicionando em suas respectivas listas
        valores = linha.strip().split(",")
        densidade_picos_coly.append(float(valores[0]))
        tempo_intervalo_colx.append(float(valores[1]))

# Leitura dos dados do arquivo "diametro_por_tempo.txt"
with open("arquivos_gerados/diametro_por_tempo.txt", "r") as arquivo:
    # Pula o cabeçalho
    next(arquivo)
    for linha in arquivo:
        # Separa os valores da variável 'valores'
        valores = linha.strip().split(",")
        lista_diam_coly.append(float(valores[0]))

# Plotando o gráfico de densidade de picos
plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]

tam_font = 16

plt.figure(figsize=(10, 6))
plt.plot(tempo_intervalo_colx, densidade_picos_coly)
plt.title("Densidade de picos por intervalo de tempo", fontsize=tam_font)
plt.xlabel("Tempo (s)", fontsize=tam_font)
plt.ylabel(r"$\langle \rho \rangle$", fontsize=tam_font)
plt.xticks(fontsize=tam_font)
plt.yticks(fontsize=tam_font)
plt.grid(True)
# plt.savefig("graficos/graf_densidade_picos.pdf", bbox_inches="tight")
# plt.show(block=False)

# Diâmetro médio
diam_final = np.mean(lista_diam_coly[7765:])  # Intervalo da análise [250s:]
diam_final_str = f"{diam_final:.2f}".replace(".", ",")
print(f"Diâmetro médio: {diam_final_str} nm")

# Plotando o gráfico de diâmetros
plt.figure(figsize=(10, 6))
plt.plot(tempo_intervalo_colx, lista_diam_coly, label="Dados de Diâmetro")
# plt.title("Diâmetro por intervalo de tempo", fontsize=tam_font)
plt.legend([rf"$\langle d_h \rangle$ = {diam_final_str} nm"], fontsize=tam_font)
plt.xlabel("Tempo (s)", fontsize=tam_font)
plt.ylabel("Diâmetro hidrodinâmico (nm)", fontsize=tam_font)
plt.xticks(fontsize=tam_font)
plt.yticks(fontsize=tam_font)
plt.grid(True)
plt.savefig("graficos/graf_diametros_dados_filtrados.pdf", bbox_inches="tight")
# plt.show()
