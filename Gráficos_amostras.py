import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import matplotlib.font_manager as fm


# Função para ler dados de um arquivo e retornar a lista de valores da segunda coluna
def ler_dados(arquivo_caminho, max_linhas=125000):
    dados_col2 = []
    with open(arquivo_caminho, "r") as arquivo:
        leitor_csv = csv.reader(arquivo)
        for _ in range(16):  # Pula as primeiras 16 linhas
            next(leitor_csv)

        linhas_lidas = 0
        for linha in leitor_csv:
            if linha:
                dados_col2.append(float(linha[1]))  # Converte os dados para float
            linhas_lidas += 1
            if linhas_lidas >= max_linhas:
                break
    return dados_col2


# Caminhos dos arquivos
arquivos = [
    "Dados/APD/xx-07-2024/amostra1_1.70/T0020CH4.CSV",
    "Dados/APD/xx-07-2024/amostra2_1.60/T0030CH4.CSV",
    "Dados/APD/04-06-2024/300nm concent.80-1 20g temp.22 T0053CH4.CSV",
]

# Constante de intervalo de tempo
intervalo_tempo = 0.0032

# Lista para armazenar os dados de cada arquivo
dados_amostras = []

# Ler os dados de cada arquivo
for arquivo in arquivos:
    dados = ler_dados(arquivo)
    dados_amostras.append(dados)

# Carregar a fonte Times New Roman explicitamente
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()

# Criando subplots
fig, axs = plt.subplots(len(arquivos), 1, figsize=(22, 12))

# Definindo o tamanho da fonte
tam_font = 36

# Função para formatar os valores do eixo y com duas casas decimais
formatter = FuncFormatter(lambda x, _: f"{x:.2f}")

# Plotando os dados em subplots separados
for i, dados in enumerate(dados_amostras):
    # Gerando o eixo x como tempo
    tempo = [indice * intervalo_tempo for indice in range(len(dados))]

    # Plotando e ajustando as fontes dos gráficos
    axs[i].plot(tempo, dados, label=f"Amostra {i+1}")
    axs[i].set_xlabel("Tempo (s)", fontsize=tam_font, fontproperties=prop)
    axs[i].set_ylabel("Intensidade", fontsize=tam_font, fontproperties=prop)
    axs[i].legend(fontsize=tam_font, loc="upper right")
    axs[i].tick_params(axis="both", which="major", labelsize=tam_font)
    axs[i].yaxis.set_major_formatter(formatter)  # Aplicando a formatação ao eixo y
    axs[i].grid(True)

    # Definindo os ticks do eixo y para exibir exatamente 3 valores
    ymin, ymax = min(dados), max(dados)
    ticks = np.linspace(ymin, ymax, 3)  # Gera 3 ticks igualmente espaçados
    axs[i].set_yticks(ticks)

# Ajustando o layout para evitar sobreposição
plt.tight_layout()

# Salvando o gráfico como PDF
plt.savefig("graficos/graf_sinal_amostras.pdf", bbox_inches="tight")

# Exibindo o gráfico
# plt.show()
