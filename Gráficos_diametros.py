import matplotlib.pyplot as plt
import numpy as np


def carregar_dados(arquivo):
    diamentros = []
    tempos = []
    with open(arquivo, "r") as a:
        next(a)
        for linha in a:
            dados = linha.strip().split(",")
            diamentros.append(float(dados[0]))
            tempos.append(float(dados[1]))
    return diamentros, tempos


diametros_A1, tempos_A1 = carregar_dados(
    "/home/dhett/Documentos/arquivos_diametros/diametro_por_tempo_120nm.txt"
)
diametros_A2, tempos_A2 = carregar_dados(
    "/home/dhett/Documentos/arquivos_diametros/diametro_por_tempo_226nm.txt"
)
diametros_A3, tempos_A3 = carregar_dados(
    "/home/dhett/Documentos/arquivos_diametros/diametro_por_tempo_300nm.txt"
)
diametros_ruido, tempos_ruido = carregar_dados(
    "/home/dhett/Documentos/arquivos_diametros/diametro_por_tempo_ruido.txt"
)

diam_final_A1 = np.mean(diametros_A1[6202:])  # Intervalo da análise [200s:]
diam_final_A2 = np.mean(diametros_A2[6202:])
diam_final_A3 = np.mean(diametros_A3[6202:])
diam_final_ruido = np.mean(diametros_ruido[6202:])

print(f"Diâmetro médio da amostra 1: {diam_final_A1:.2f} nm")
print(f"Diâmetro médio da amostra 2: {diam_final_A2:.2f} nm")
print(f"Diâmetro médio da amostra 3: {diam_final_A3:.2f} nm")

plt.rcParams["font.family"] = ["DeJavu Serif"]
plt.rcParams["font.serif"] = ["Times New Roman"]

tam_font = 10

plt.figure(figsize=(10, 6))
plt.plot(tempos_A1, diametros_A1, label=rf"A1, $d_h = {diam_final_A1:.2f} nm$")
plt.plot(tempos_A2, diametros_A2, label=rf"A2, $d_h = {diam_final_A2:.2f} nm$")
plt.plot(tempos_A3, diametros_A3, label=rf"A3, $d_h = {diam_final_A3:.2f} nm$")
plt.plot(tempos_ruido, diametros_ruido, label=rf"R, $d_h = {diam_final_ruido:.2f} nm$")

plt.title("Diâmetro por tempo", fontsize=tam_font)
plt.xlabel("Tempos (s)", fontsize=tam_font)
plt.ylabel("Diâmetro hidrodinâmico (nm)", fontsize=tam_font)
plt.xticks(fontsize=tam_font)
plt.yticks(fontsize=tam_font)
plt.legend(loc="upper center", fontsize=tam_font, ncols=4)
plt.grid(True)
plt.savefig(
    "/home/dhett/Documentos/arquivos_diametros/graf_diâmetros_das_amostras.svg",
    bbox_inches="tight",
)
plt.show()
