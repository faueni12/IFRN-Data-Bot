import pandas as pd
from tabula import read_pdf
from unidecode import unidecode

from Settings_IFRN import *


# Facilitar e organizar o acesso aos dados pelo dicionário dic
def ALL(df, **kwargs):
    cota = kwargs.get('cota')
    
    dic = {'media':df['Score'].mean(),
            'moda':df['Score'].mode(),
            'maior':df['Score'].max(),
            'desvio':df['Score'].std(),
            'menor':df['Score'].min()}
    
    if cota:
        dic['menor_cota'] = df.loc[df['Cota'] == cota]['Score'].min()
        dic['maior_cota'] = df.loc[df['Cota'] == cota]['Score'].max()
         
    return dic


# Lê e Organiza os Dados do PDF
# Se for possível, depois passar pra um banco de dados e diminuir o processamento...
def LerDado(PDF, qt_curso, iterador):
    df = read_pdf(PDF, output_format='csv', pages='all')
    # Renomear Colunas
    df.columns = ['Matricula', 'Nome', 'Lugar', 'Cota', 'Score']
    info = {'name':list(df['Nome']), 
            'score':list(df['Score']),
            'cota':list(df['Cota'])}

    # Mostrar Curso e Score
    cursos = []
    i = 0
    for y in range(qt_curso):
            curso = next(iterador)
            
            qt_aluno = 0
            while i < len(df):
                i += 1
                qt_aluno += 1

                # Try é gambiarra
                try:
                    # Se o Nome estiver em Ordem Crescente
                    if  unidecode(info['name'][i][0]) > unidecode(info['name'][i+1][0]):
                        i+=1
                        qt_aluno += 1
                        cursos += [str(curso[:3])]*qt_aluno
                        break
                except:
                    i+=1
                    qt_aluno += 1
                    cursos += [str(curso[:3])]*qt_aluno
                
    # Acrescentar os Cursos de cada aluno no dataframe:
    df['Curso'] = cursos

    lista = []
    for i in df['Score']:
        lista += [i[:3]]
    lista = list(map(int, lista))
    df['Score'] = lista

    return df
