# -----------------------------------------------------
# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# -----------------------------------------------------
#
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Tema: Simulação Aeropêndulo
# Autor: Oséias Farias
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
#
# Data: 2023
#  ----------------------------------------------------
#
import vpython as vp
from typing import Tuple


class Graficos:
    """
    Gráfico para polagem dos dados dos estados do Aeroèndulo.
    """
    def __init__(self, largura=650, altura=400):
        self.width = largura
        self.height = altura

    def graficos(self) -> Tuple:
        """
        Método que cria os Gráfico.

        Returns:
            Retorna uma tupla contendo o objeto do gráfico e da curvas.
        """
        titulo = "Gráficos dos estados do Aeropêndulo"
        self.grafico = vp.graph(title=titulo, align="right",
                                xtitle='tempo (s)', fast=True,
                                width=self.width, height=self.height,
                                center=vp.vector(0, 12, 0), scroll=True,
                                xmin=0, xmax=14, ymin=-0.5, ymax=6, dot=True,
                                background=vp.vector(0.95, 0.95, 0.95))

        self.curva1 = vp.gcurve(color=vp.color.blue, width=3,
                                markers=False, label="Posição Angular (rad)",
                                dot=True, dot_color=vp.color.blue)

        self.curva2 = vp.gcurve(color=vp.color.black, width=3, markers=False,
                                label="Referência Angular(rad)", dot=True,
                                dot_color=vp.color.black)

        self.curva3 = vp.gcurve(color=vp.color.red, width=3, markers=False,
                                label="Velocidade Angular (rad/s)", dot=True,
                                dot_color=vp.color.red)

        self.curva4 = vp.gcurve(color=vp.color.orange, width=3, markers=False,
                                label="Sinal de Controle (V)", dot=True,
                                dot_color=vp.color.orange)

        return self.grafico, self.curva1, self.curva2, self.curva3, self.curva4
