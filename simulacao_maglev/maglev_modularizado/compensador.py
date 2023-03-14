import control as ct
import numpy as np


# %% Projeto do Compensador
class Compensador:
    def __init__(self, planta, P, Q):

        # Ordem do sistema
        n = planta.A.shape[0]

        # Projeto numérico do regulador integral
        Aa = np.block([[planta.A, np.zeros((n, 1))], [-planta.C, 0]])
        Ba = np.block([[planta.B], [0]])
        Ka = ct.acker(Aa, Ba, P)
        K = Ka[:, :n]
        Ki = Ka[:, n]

        # Projeto numérico do observador
        L = ct.acker(planta.A.T, planta.C.T, Q).T

        # Matrizes para implementação do compensador
        Ar = np.block(
            [[planta.A-planta.B@K-L@planta.C, -planta.B*Ki], [np.zeros((1, n+1))]])
        Br = np.block([[L, np.zeros((n, 1))], [-1, 1]])

        # Armazena atributos do objeto
        self.Ar = Ar
        self.Br = Br
        self.K = K[0, :]
        self.Ki = Ki
        self.Ka = Ka[0, :]
        self.L = L

    # Definindo os sinais de referência para rastreamento
    @staticmethod
    def ref_seno(t):
        return (mag.x0*np.sin(2*pi*t))

    @staticmethod
    def ref_quad(t):
        return (mag.x0)*(np.sin(2*pi*t) >= 0)