# Esta versão do scrip é capaz de calcular a autocorrelação e a correlação cruzada
# de vários arquivos de uma única vez.

import numpy as np
from tqdm import tqdm

# Lista dos arquivos para processar
arquivos_originais = [
    f"dados_processados/dados_originais_M{i}.txt" for i in range(1, 11)
]
arquivos_filtrados = [
    f"dados_processados/dados_filtrados_M{i}.txt" for i in range(1, 11)
]

# Lista para armazenar os resultados da correlação cruzada
resultados_correlacao_cruzada = []

# Processa cada par de arquivos usando uma única barra de progresso
with tqdm(total=len(arquivos_originais), desc="Calculando correlação") as pbar:
    for arquivo_orig, arquivo_filt in zip(arquivos_originais, arquivos_filtrados):
        # Carrega os dados dos arquivos .txt
        carregar_originais = np.loadtxt(arquivo_orig, delimiter=",")
        carregar_filtrados = np.loadtxt(arquivo_filt, delimiter=",")

        # Separa as colunas em variáveis distintas
        dados_originais = carregar_originais[:, 0]
        dados_filtrados = carregar_filtrados[:, 0]

        # Calcula a média e a correlação cruzada entre dados originais e filtrados
        media_dados_originais = np.mean(dados_originais)
        media_dados_filtrados = np.mean(dados_filtrados)
        correlacao_cruzada = np.correlate(
            dados_originais - media_dados_originais,
            dados_filtrados - media_dados_filtrados,
            mode="full",
        ) / (len(dados_originais) * np.std(dados_originais) * np.std(dados_filtrados))

        # Armazena o primeiro valor da correlação cruzada
        altura_correlacao_cruzada = correlacao_cruzada[len(dados_originais) - 1]
        altura_correlacao_cruzada_str = f"{altura_correlacao_cruzada:.3f}".replace(
            ".", ","
        )
        resultados_correlacao_cruzada.append(altura_correlacao_cruzada_str)

        # Atualiza a barra de progresso
        pbar.update(1)

# Imprime os resultados da correlação cruzada
lista_correl_cruz = []
print("\nResultados da correlação cruzada para cada medida")
print("-" * 50)
for i, resultado in enumerate(resultados_correlacao_cruzada, start=1):
    medida_str = f"M{i:02d}"  # Formata para M01, M02, ..., M10
    print(f"{medida_str}: {resultado}")
    lista_correl_cruz.append(float(resultado.replace(",", ".")))

media_correl_cruz = np.mean(lista_correl_cruz)
media_correl_cruz_str = f"{media_correl_cruz:.3f}".replace(".", ",")
print(f"\nMédia = {media_correl_cruz_str}")
print("-" * 50)
