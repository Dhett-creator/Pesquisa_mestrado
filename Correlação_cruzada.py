import matplotlib.pyplot as plt
import numpy as np

# Carrega os dados dos arquivos .txt
carregar_originais = np.loadtxt("dados_processados/dados_originais.txt", delimiter=",")
carregar_filtrados = np.loadtxt("dados_processados/dados_filtrados.txt", delimiter=",")

# Separa as colunas em variáveis distintas
dados_originais = carregar_originais[:, 0]  # Primeira coluna
tempo_originais = carregar_originais[:, 1]  # Segunda coluna

dados_filtrados = carregar_filtrados[:, 0]  # Primeira coluna
tempo_filtrados = carregar_filtrados[:, 1]  # Segunda coluna

# Calcula a média e a autocorrelação dos dados originais
media_dados_originais = np.mean(dados_originais)
autocorrelacao1 = np.correlate(
    dados_originais - media_dados_originais,
    dados_originais - media_dados_originais,
    mode="full",
) / (len(dados_originais) * np.var(dados_originais))

# Calcula a média e a autocorrelação dos dados filtrados
media_dados_filtrados = np.mean(dados_filtrados)
autocorrelacao2 = np.correlate(
    dados_filtrados - media_dados_filtrados,
    dados_filtrados - media_dados_filtrados,
    mode="full",
) / (len(dados_filtrados) * np.var(dados_filtrados))

# Calcula a correlação cruzada entre dados originais e filtrados
media_dados_originais = np.mean(dados_originais)
media_dados_filtrados = np.mean(dados_filtrados)
correlacao_cruzada = np.correlate(
    dados_originais - media_dados_originais,
    dados_filtrados - media_dados_filtrados,
    mode="full",
) / (len(dados_originais) * np.std(dados_originais) * np.std(dados_filtrados))

# Imprime o primeiro valor/altura da correlação cruzada
altura_correlacao_cruzada = correlacao_cruzada[len(dados_originais) - 1]
altura_correlacao_cruzada_str = f"{altura_correlacao_cruzada:.3f}".replace(".", ",")
print(f'\n"Altura da correlação cruzada: {altura_correlacao_cruzada_str}')

# Limita o tamanho do lag desejado
max_lag = 500
autocorrelacao1 = autocorrelacao1[
    len(dados_originais) - 1 : len(dados_originais) + max_lag
]
autocorrelacao2 = autocorrelacao2[
    len(dados_filtrados) - 1 : len(dados_filtrados) + max_lag
]
correlacao_cruzada = correlacao_cruzada[
    len(dados_originais) - 1 : len(dados_originais) + max_lag
]

# Plotar o gráfico de autocorrelação e correlação cruzada
lags = np.arange(0, max_lag + 1)

plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]

tam_font = 16

plt.figure(figsize=(10, 6))

plt.plot(lags, autocorrelacao1, label="Autocorrelação dos dados originais")
plt.plot(lags, autocorrelacao2, label="Autocorrelação dos dados filtrados")
plt.plot(
    lags,
    correlacao_cruzada,
    label=f"Correlação cruzada; Altura = {altura_correlacao_cruzada_str} ",
    linestyle="--",
)
# plt.title("Autocorrelação e Correlação Cruzada", fontsize=tam_font)
plt.xlabel("Lag", fontsize=tam_font)
plt.ylabel("Correlação", fontsize=tam_font)
plt.legend(fontsize=tam_font)
plt.xticks(fontsize=tam_font)
plt.yticks(fontsize=tam_font)
plt.grid(True)
plt.savefig("graficos/graf_correlacao_cruzada.pdf", bbox_inches="tight")
# plt.show()
