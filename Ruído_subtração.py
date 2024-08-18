import csv
import matplotlib.pyplot as plt


def leitura(caminho_arquivo):
    lista_dados = []

    with open(caminho_arquivo, newline='') as arquivo_csv:
        ler_arquivo = csv.reader(arquivo_csv, delimiter=',')
        # next(ler_arquivo, None)

        for linha_numero, linha in enumerate(ler_arquivo, start=1):
            if linha_numero >= 17 and len(linha) >= 2:
                try:
                    dados_coluna2 = float(linha[1])
                    lista_dados.append(dados_coluna2)
                except ValueError:
                    print(f'A linha {linha_numero} possui um valor inválido!')

    return lista_dados


diretorio_sinal = 'Dados/FD/30-04-2024/T0011CH1-300nm-concent.70_1-20graus-22temp.csv'
diretorio_ruido = 'Dados/FD/30-04-2024/T0012CH1-ruido-concent.70_1-20graus-22temp.csv'
dados_sinal = leitura(diretorio_sinal)
dados_ruido = leitura(diretorio_ruido)

print(f'\nA lista de dados relacionados ao "sinal captado" pelo sensor possui {len(dados_sinal)} elementos.')
print(f'A lista de dados relacionados ao ruído de fundo captado pelo sensor possui {len(dados_ruido)} elementos.')

lista_subtracao_ruido = []
for a, b in zip(dados_sinal, dados_ruido):
    subtracao = a - b
    lista_subtracao_ruido.append(subtracao)

print(f'A lista de dados relacionados à subtração do ruído do sinal possui {len(lista_subtracao_ruido)} elementos.')

lista_tempo = []
cont = 0
for i in range(0, len(lista_subtracao_ruido), 1):
    if i == 0:
        lista_tempo.append(cont)
    else:
        cont += 0.0032
        lista_tempo.append(cont)

print(f'A lista de dados relacionados ao tempo de aquisição dos dados possui {len(lista_subtracao_ruido)} elementos.\n')

diretorio_salvamento = 'dados_processados/ruído_subtração.txt'
with open(diretorio_salvamento, mode='w', newline='') as arquivo:
    escrever = csv.writer(arquivo, delimiter=',')

    for linha in zip(lista_subtracao_ruido, lista_tempo):
        escrever.writerow(linha)

print(f'Dados escritos com sucesso em "{diretorio_salvamento}"!')

fig, axs = plt.subplots(3, 1, figsize=(12, 6))

axs[0].plot(lista_tempo, dados_sinal, label='gráfico1', color='black')
axs[0].set_title('Gráfico 1 - Sinal captado')

axs[1].plot(lista_tempo, dados_ruido, label='gráficos2', color='black')
axs[1].set_title('Gráfico 2 - Ruído')

axs[2].plot(lista_tempo, lista_subtracao_ruido, label='gráfico3', color='black')
axs[2].set_title('Gráfico 3 - Subtração do Ruído')

plt.tight_layout()
plt.savefig('graficos/graf_subtracao_ruido.pdf')
