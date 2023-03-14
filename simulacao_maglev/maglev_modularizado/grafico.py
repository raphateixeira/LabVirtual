from vpython import *


class Grafico:
    def __init__(self):
        self.graficos()  

    def graficos(self):
        # Criando o gráfico para mostrar os sinais
        self.grafico = graph(width=700, height=400, align='right',
                             title='Resposta do sistema a um sinal de referência',
                             xtitle='Tempo (s)', ytitle='Posição (mm)', fast=False,
                             scroll=True, xmin=0, xmax=5)
        # Curva da posição real
        self.yplot = gdots(color=color.red, size=2, label='Sistema')
        # Curva do sinal de referência
        self.rplot = gcurve(color=color.blue, label='Referência')

        # %% Criação da legenda flutuante

        self.legenda_1 = label(pos=vec(0, 11.5e-2, 0),
                               text="<b>O cilindro está na posição inicial!</b>",
                               font="Verdana")
