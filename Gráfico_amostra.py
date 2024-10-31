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


# Caminho do arquivo único
arquivo = "Dados/APD/27-05-2024/226nm concent.100-1 20g temp.22 T0034CH4.CSV"

# Constante de intervalo de tempo
intervalo_tempo = 0.0032

# Ler os dados do arquivo
dados = ler_dados(arquivo)

# Carregar a fonte Times New Roman explicitamente
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"  # Diretório de fontes no ubuntu
# font_path = "/usr/share/fonts/TTF/Times.TTF" # Diretório de fontes no archlinux
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()

# Criando o gráfico
fig, ax = plt.subplots(figsize=(22, 5))  # (x, y)

# Definindo o tamanho da fonte
tam_font = 35

# Função para formatar os valores do eixo y com duas casas decimais
formatter = FuncFormatter(lambda x, _: f"{x:.2f}")

# Gerando o eixo x como tempo
tempo = [indice * intervalo_tempo for indice in range(len(dados))]

# Plotando e ajustando as fontes do gráfico
ax.plot(tempo, dados, label="Amostra 1")
ax.set_xlabel("Tempo (s)", fontsize=tam_font, fontproperties=prop)
ax.set_ylabel("Intensidade", fontsize=tam_font, fontproperties=prop)
# ax.legend(fontsize=tam_font, loc="upper right")
ax.tick_params(axis="both", which="major", labelsize=tam_font)
ax.yaxis.set_major_formatter(formatter)  # Aplicando a formatação ao eixo y
ax.grid(True)

# Definindo os ticks do eixo y para exibir exatamente 3 valores
ymin, ymax = min(dados), max(dados)
ticks = np.linspace(ymin, ymax, 4)  # Gera 3 ticks igualmente espaçados
ax.set_yticks(ticks)

# Ajustando o layout para evitar sobreposição
plt.tight_layout()

# Salvando o gráfico como PDF
plt.savefig("graficos/graf_sinal_amostra.pdf", bbox_inches="tight")

# Exibindo o gráfico
# plt.show()
