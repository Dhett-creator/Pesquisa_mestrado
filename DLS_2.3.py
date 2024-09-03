# Além de analisar 10 medidas de uma única vez, essa versão do script consegue
# realizar a contagem de picos de forma mais rápida que as versões anteriores.

import math
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import find_peaks  # Importa a função find_peaks do scipy

# Listas para armazenar todas as curvas e médias de diâmetros
todas_densidades = []
todas_diametros = []
medias_diametros = []
tempo_intervalo_colx = (
    None  # Para garantir que o tempo seja o mesmo para todas as curvas
)

# Definir o intervalo para calcular a média dos diâmetros (substitua pelos índices corretos)
intervalo_inicio = 7765  # Exemplo: 250s
intervalo_fim = None  # Até o final

# Loop para processar os arquivos dados_filtrados_M1 a dados_filtrados_M10
for i in tqdm(
    range(1, 11), desc="Processando arquivos"
):  # Adiciona a barra de progresso aqui
    # Leitura do arquivo.txt correspondente
    dados_leitura = np.loadtxt(
        f"dados_processados/dados_filtrados_M{i}.txt", delimiter=","
    )
    col1 = dados_leitura[:, 0].astype(float).tolist()  # Dados de intensidade luminosa
    col2 = dados_leitura[:, 1].astype(float).tolist()  # Dados de tempo

    # Intervalo de tempo entre as medições
    intervalo_tempo = col2[1] - col2[0]

    # Listas para armazenar o número de picos e a densidade de picos
    num_picos_lista = []
    densidade_picos_lista = []
    tempo_intervalo_lista = []

    # Contagem de picos progressiva usando scipy
    for num_linhas in range(500, len(col1), 10):  # Ajustar o range conforme desejado
        dados_parciais = col1[:num_linhas]
        picos, _ = find_peaks(dados_parciais)  # Usa find_peaks para contar os picos
        num_picos = len(picos)
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

    # Calcular a média dos diâmetros no intervalo especificado
    diam_final = np.mean(list_dnm[intervalo_inicio:intervalo_fim])
    medias_diametros.append(f"{diam_final:.2f}".replace(".", ","))

    # Armazenar as curvas para plotagem
    todas_densidades.append(densidade_picos_lista)
    todas_diametros.append(list_dnm)

    # Garantir que o tempo seja o mesmo para todas as curvas
    if tempo_intervalo_colx is None:
        tempo_intervalo_colx = tempo_intervalo_lista

# Configuração das legendas do gráfico
plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]
tam_font = 16

# Plotando o gráfico de diâmetros para todas as medidas com a média na legenda
plt.figure(figsize=(12, 7))

for j, (diametros, diam_final_str) in enumerate(
    zip(todas_diametros, medias_diametros), start=1
):
    file_label = f"M{str(j).zfill(2)}"  # Formata para M01, M02, ..., M10
    plt.plot(
        tempo_intervalo_colx,
        diametros,
        label=rf"{file_label}; $\langle d_h \rangle$ = {diam_final_str} nm",
    )
plt.xlabel("Tempo (s)", fontsize=tam_font)
plt.ylabel("Diâmetro hidrodinâmico (nm)", fontsize=tam_font)
plt.xticks(fontsize=tam_font)
plt.yticks(fontsize=tam_font)
plt.grid(True)

# Ajuste das legendas no canto superior direito com duas colunas de cinco linhas
plt.legend(
    fontsize=tam_font,
    loc="upper right",  # Posição no canto superior direito
    ncol=2,  # Número de colunas
    bbox_to_anchor=(1, 1),  # Ajusta a posição para o canto superior direito
    title_fontsize=tam_font,  # Tamanho da fonte do título
)

plt.savefig(
    "graficos/graf_diametros_dados_filtrados_todas_medidas.pdf", bbox_inches="tight"
)
# plt.show()
