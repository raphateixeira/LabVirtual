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
#  ----------------------------------------------------
#
import vpython as vp
from typing import Tuple


class Graficos:
    """
    Gráfico para polagem dos dados dos estados do Aeroèndulo.

    """
    def __init__(self):
        ...

    def graficos(self) -> Tuple:
        """
        Método que cria os Gráfico.

        Returns:
            Retorna uma tupla contendo o objeto do gráfico e da curvas.
        """
        titulo = "Gráficos dos estados do Aeropêndulo"
        self.grafico = vp.graph(title=titulo, align="right",
                                xtitle='tempo (s)', fast=True, width=650,
                                height=450, center=vp.vector(0, 12, 0),
                                scroll=True, xmin=0, xmax=5, ymin=-5, ymax=5,
                                dot=True, background=vp.vector(0.95,
                                                               0.95, 0.95))

        self.curva1 = vp.gcurve(color=vp.color.blue, width=3,
                                markers=False, label="Posição Angular",
                                dot=True, dot_color=vp.color.blue)

        self.curva2 = vp.gcurve(color=vp.color.red, width=3, markers=False,
                                label="Velocidade Angular",
                                dot=True, dot_color=vp.color.red)

        # curva3 = vp.gcurve(color=vp.color.orange, width=3, markers=False,
        #                    label="Aceleração Angular do Pêndulo",
        #                    dot=True, dot_color=vp.color.orange)
        return self.grafico, self.curva1, self.curva2

    def reset(self):
        self.curva1.delete()
        self.curva2.delete()
        self.grafico.xmin = 0
        self.grafico.xmax = 5
