import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Carrega os dados dos 'arquivos.csv'
carregar_originais = np.loadtxt("dados_processados/dados_originais1.txt", delimiter=",")
carregar_filtrados = np.loadtxt("dados_processados/dados_originais.txt", delimiter=",")

# Separa as colunas em variáveis distintas
dados_originais = carregar_originais[:, 0]  # Primeira coluna
tempo_originais = carregar_originais[:, 1]  # Segunda coluna

dados_filtrados = carregar_filtrados[:, 0]  # Primeira coluna
tempo_filtrados = carregar_filtrados[:, 1]  # Segunda coluna

# Calcula a média e a autocorrelação dos dados
media_dados_originais = np.mean(dados_originais)
autocorrelacao1 = np.correlate(
    dados_originais - media_dados_originais,
    dados_originais - media_dados_originais,
    mode="full",
) / (len(dados_originais) * np.var(dados_originais))

media_dados_filtrados = np.mean(dados_filtrados)
autocorrelacao2 = np.correlate(
    dados_filtrados - media_dados_filtrados,
    dados_filtrados - media_dados_filtrados,
    mode="full",
) / (len(dados_filtrados) * np.var(dados_filtrados))

# Limita o tamanho do lag desejado
max_lag = 500
autocorrelacao1 = autocorrelacao1[
    len(dados_originais) - 1 : len(dados_originais) + max_lag
]
autocorrelacao2 = autocorrelacao2[
    len(dados_filtrados) - 1 : len(dados_filtrados) + max_lag
]

# Plotar o gráfico de autocorrelação
lags = np.arange(0, max_lag + 1)

plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]

tam_font = 16

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(lags, autocorrelacao1, label="Concentração = 1:70 mL", color="black")
ax.plot(lags, autocorrelacao2, label="Concentração = 1:60 mL", color="C3")
ax.set_xlabel("Lag", fontsize=tam_font)
ax.set_ylabel("Autocorrelação", fontsize=tam_font)
ax.legend(fontsize=tam_font)
ax.tick_params(axis="both", which="major", labelsize=tam_font)
ax.grid(True)

# Criar o gráfico inset com zoom
ax_inset = ax.inset_axes([0.35, 0.25, 0.25, 0.5], xlim=(-24, 30), ylim=(0.75, 1))
ax_inset.plot(lags, autocorrelacao1, lw=2.5, color="black")
ax_inset.plot(
    lags,
    autocorrelacao2,
    lw=2.5,
    color="C3",
)
ax_inset.set_xticklabels([])  # Remove os ticks do eixo x
ax_inset.set_yticklabels([])  # Remove os ticks do eixo y
ax_inset.grid(True)

# Destacar a área de zoom
ax.indicate_inset_zoom(ax_inset, edgecolor="black")

plt.savefig("graficos/graf_autocorrelacao.pdf", bbox_inches="tight")
# plt.show()
