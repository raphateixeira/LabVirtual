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

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from typing import List, Annotated, Literal, TypeVar
import numpy.typing as npt

plt.style.use("ggplot")

# Typing annotation array numpy
DType = TypeVar("DType", bound=np.generic)
Array1XN = Annotated[npt.NDArray[DType], Literal[1, "N"]]


class ModeloMatAeropendulo(object):
    """
    Modelo Matemático do Aeropêndulo para simulação dinâmica

    Args:
        x_0: Condições iniciais para simulação.
        K_m: float
        m: Massa total do Aeroèndulo (braço + Motor + Hélices).
        d: Tamanho do Braço do Aeropêndulo.
        J: Momento de Inércia do Aeropêndulo.
        c: coeficente de atrito do Aeropêndulo.
    """

    def __init__(self, x_0: List[float] = [0.1, -0.5], K_m: float = 0.0296,
                 m: float = 0.36, d: float = 0.03, J: float = 0.0106,
                 c: float = 0.0076) -> None:
        # Parâmetros do Aeropêndulo.
        self.K_m = K_m
        self.m = m
        self.d = d
        self.J = J
        self.g = 9.8
        self.c = c

        # Configuração para simulação
        self.t: Array1XN
        self.x = x_0
        self.x1: List[List[float]] = [[], []]

        # Sinulação
        self.simu = False
        self.simu_dinamic = False

    def modelo_aeropendulo(self, x: List[float], t: Array1XN) -> Array1XN:
        """
        Método que implementa o modelo matemático do aeropêndulo.
        Args:
            x: Estados atuais do sistema.
            t: necessário caso use scipy.integrate.odeint
        Returns:
            Retorna um array numpy contendo a derivada dos estados.
        """
        x1, x2 = x        # Variáveis de estado a partir do vetor de estados;
        dx1 = x2          # Função de estado dx1 = f(x,u)

        # Função de estado dx2 = f(x,u)
        dx2 = -(self.m*self.g*self.d/self.J)*x1-(self.c/self.J)*x2 +\
               (self.K_m/self.J)*4.
        dx = np.array([dx1, dx2])      # Derivada do vetor de estados
        return dx                      # Retorna a derivada do vetor de estados

    def simular(self, t_simu: int = 100, ts: float = 0.1,
                x_0: List[float] = [0.1, -0.5]) -> None:
        """
        Método que implementa uma simulação com scipy.integrate.odeint,
        no final plota os gráficos dos estados do sistema para a dada
        simulação.
        Args:
            t_simu: tempo de simulação, Padrão: 100.
            ts: Período de amostragem, Padrão: 0.1
            x_0: Condições iniciais para simulação
        """
        self.simu = True
        self.t_simu = t_simu
        self.ts = ts
        self.t = ts*np.arange(0, t_simu+ts, ts)
        # Condições iniciais
        self.x_0 = x_0
        # Integração com método odeint() da biblioteca scipy.integrate
        self.x_ = odeint(self.modelo_aeropendulo, self.x_0, self.t)
        self.plotar_graficos()

    def simulacao_dinamica(self, t_simu: int = 100, ts: float = 0.1,
                           x_0: List[float] = [0.1, -0.5]) -> None:
        """
        Método que implementa uma simulação com integrtação usando o laço for,
        no final plota os gráficos dos estados do sistema para a dada
        simulação.
        Args:
            t_simu: tempo de simulação, Padrão: 100.
            ts: Período de amostragem, Padrão: 0.1
            x_0: Condições iniciais do sistema.
        """
        self.simu_dinamic = True
        self.t_simu = t_simu
        self.ts = ts
        self.t = ts*np.arange(0, t_simu+ts, ts)
        self.x = x_0
        for j, i in enumerate(self.t):
            dx = self.modelo_aeropendulo(self.x, self.t)
            try:
                dt = (self.t[j+1]-i)
            except Exception:
                pass
            self.x = self.x + dt * dx
            self.x1[0].append(self.x[0])
            self.x1[1].append(self.x[1])
        self.plotar_graficos()

    def plotar_graficos(self) -> None:
        """
        Método para plotagem dos gráficos de simulação interna, para os métodos
        simular() e simulacao_dinamica(), plota os gráficos dos estados do
        sistema, velocidade e posição.
        """
        plt.figure(figsize=(10, 7))
        plt.suptitle("Gráficos dos estados do Aeropêndulo")

        plt.subplot(211)
        if self.simu:
            plt.plot(self.t, self.x_[:, 0], lw=3.5)
        if self.simu_dinamic:
            plt.plot(self.t, self.x1[0])

        plt.subplot(212)
        if self.simu:
            plt.plot(self.t, self.x_[:, 1], lw=2)
        if self.simu_dinamic:
            plt.plot(self.t, self.x1[1])
        if self.simu or self.simu_dinamic:
            plt.show()


if __name__ == "__main__":
    aeropendulo_1 = ModeloMatAeropendulo()
    aeropendulo_1.simular(t_simu=1000, ts=1e-2)
    aeropendulo_1.simulacao_dinamica(t_simu=1000, ts=1e-2)
