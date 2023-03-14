import numpy as np


#  MODELAGEM --------------------------------------------------------------
# %% Modelagem da Planta do MAGLEV
class Maglev:
    def __init__(self, m, k, mu, I0):
        self.m = m          # Massa em kg
        self.k = k          # Constante magnética em N m^2/A^2
        self.mu = mu        # Constante magnética em m
        self.g = 9.81       # Gravidade, em m/s^2

        self.I0 = I0        # Corrente de equilíbrio, em A

        # Posição de equilíbrio, a partir da corrente
        self.x0 = np.sqrt(k*I0**2/(m*self.g))-mu

        # Parâmetros linearizados
        self.lamda = np.sqrt(2*k*I0**2/(m*(self.x0+mu)**3))
        self.a = 2*k*I0/(m*(self.x0+mu)**2)
        self.A = np.array([[0, 1.], [self.lamda**2, 0]])
        self.B = np.array([[0], [-self.a]])
        self.C = np.array([[1., 0]])
    # %% Equações de estados em malha fechada

    @staticmethod
    def estadosmf(t, x, ref, planta, comp):
        # Separa os estados do controlador
        z = x[2:]
        # Lista que vai conter os resultados
        ddt = [0.]*5
        # Corrente do imã - corrente de equilíbrio + correção do controlador
        I = planta.I0 - comp.Ka@z
        # Variação de posição em relação ao equilíbrio - precisa para o observador
        Dx1 = x[0]-planta.x0
        # Vetor contendo os sinais de entrada do controle, saída + referência
        u = [Dx1, ref(t)]
        # Planta:
        ddt[0] = x[1]
        ddt[1] = planta.g - planta.k*I**2/(planta.m*(x[0]+planta.mu)**2)
        # Controlador:
        ddt[2:] = comp.Ar@z + comp.Br@u
        return ddt
    
    # Função para implementar ruído gaussiano
    @staticmethod
    def ruido(amp):
        return amp*np.random.normal(loc=0, scale=amp)