from tabula import read_pdf
import pandas as pd
import matplotlib.pyplot as plt

from ReadData import *
from Settings_IFRN import *


df = LerDado('ifrn.pdf', 82, CURSOS_2020)

def getPhoto(dataFrame, course, **kwargs):
            cota = kwargs.get('cota')
            # Processar Dado
            dic = ALL(dataFrame, cota=cota)

            # Settings do Gráfico
            plt.figure(figsize=(5,5),dpi=70)
            plt.plot(2020, dic['media'], marker='.', label='media')
            plt.plot(2020, dic['desvio'], marker='.', label='desvio')
            plt.plot([2020]*len(dic['moda']),
                     dic['moda'], marker='.', label='moda')

            if cota:
                plt.plot(2020, dic['maior_cota'], marker='*', label='maior nota')
                plt.plot(2020, dic['menor_cota'], marker='x', label='menor nota')
            else:
                plt.plot(2020, dic['maior'], marker='.', label='maior nota')
                
            plt.ylabel("Valor")
            plt.xlabel("Ano")
            if cota:
                plt.title('Dados - {} {} {} - {}'.format(course[0], course[1], course[2], cota), fontsize=10)
            else:
                plt.title('Dados - {} {} {}'.format(course[0], course[1], course[2]), fontsize=10)
    
            plt.legend()

            # Save Photo
            name_ph = 'dado.png'
            plt.savefig(name_ph)
            # Send Photo
            photo = open(name_ph, 'rb')

            return photo
