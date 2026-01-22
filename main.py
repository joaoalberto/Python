"""
tratamento para listas de livros em prateleiras do goodreads
joao af oliveira - dez/2023
"""
import copy


def ler_arquivo(arquivo):
  """
  Lê um arquivo txt de series e retorna uma lista com as linhas lidas.
  Ex. formato linha saida: [to-read, amazon, experiment-x-2]
  """
  with open(arquivo, "r") as f:
    linhas = f.readlines()

  print('lidos', len(linhas))

  return linhas


def gravar_arquivo(arquivo, linhas):
  """
  Grava uma lista em um arquivo txt eliminando linhas vazias
  Ex. formato entrada: [to-read, amazon, experiment-x-2]
  Ex. formato saida: 'to-read,amazon,experiment-x-2'+\n
  """

  i = 0
  with open(arquivo, "w") as f:
    for linha in linhas:
      if linha != '\n' and len(linha) > 0:
        f.write(linha.rstrip() + "\n")
        i += 1

  print('gravados', i)


def limpar_listas(lista):
  """Limpa todas as ocorrências de uma string de uma lista"""

  strings = [
      'to-read', 'amazon', 'kobo', 'googlebooks', 'tor', 'ibooks',
      'currently-reading', 'collections', ','
  ]

  lista_nova = []
  for linha in lista:
    achou = False

    for string in strings:
      if string == linha:
        achou = True
        break

    if not achou:
      lista_nova.append(linha)

  return lista_nova


def separar_series(lista):
  """
  Separa as series dentro de uma mesma linha gravando nova lista com uma serie por linha
  """

  lista_nova = []
  for linha in lista:
    linha = linha.replace(',', '')
    livro = linha.split()
    for l in livro:
      lista_nova.append(l)

  return lista_nova


def contar_livros(lista, lista_repetidos):
  """Conta as ocorrencias de um livro na lista"""

  lista_contagem = []
  for livro in lista:
    cont = lista_repetidos.count(livro)
    linha = livro + ',' + str(cont)
    lista_contagem.append(linha)

  return lista_contagem


def extrair_max_series(lista):
  """Conta as ocorrencias de um livro na lista"""

  lista_max = []
  for linha in linhas:
    partes = linha.split(
        "-")  # tratamento para quant maxima de livros na lista
    ultima_parte = partes[-1]

    linha_nova = ''
    for parte in partes:
      if parte != ultima_parte:
        linha_nova = parte if linha_nova == "" else linha_nova + "-" + parte

    linha_max = linha_nova + ',' + ultima_parte
    lista_max.append(linha_max)

  return lista_max


if __name__ == "__main__":
  file_in = "bookshelves.txt"
  file_out = "series_completas.txt"

  print("EXTRAINDO SERIES COMPLETAS\n")
  
  linhas = ler_arquivo(file_in)
  linhas = separar_series(linhas)  # lista livros uma por linha
  livros_repetidos = copy.deepcopy(linhas)  # copia a lista de livros

  linhas = set(linhas)  # retirar duplicidade
  linhas = sorted(linhas)  # ordenar as linhas
  linhas = limpar_listas(linhas)  # limpar as linhas indesejadas
  #gravar_arquivo(arquivo1, linhas)  # grava arquivo com as listas de livros

  livros_contagem = contar_livros(linhas, livros_repetidos)
  #gravar_arquivo(arquivo2, livros_contagem)
  #print(livros_contagem)

  linhas = extrair_max_series(linhas)  # lista de livros com maximo serie
  #gravar_arquivo(arquivo3, linhas)
  #print(linhas)

  novalista = [
      linha for linha, contagem in zip(linhas, livros_contagem)
      if linha.split(",")[1] == contagem.split(",")[1]
  ]
  
  gravar_arquivo(file_out, novalista)  # grava arquivo com as series completas

  