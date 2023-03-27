
class ControladorDiscreto:
    def __init__(self, referencia=1, T=0.0625):
        self.uk = 0
        self.uk1 = 0
        self.ek = 0
        self.ek1 = 0
        self.yout = 0
        self.k = 0
        self.r = referencia
        self.T = T

    # Pega o sinal do sensor
    def sensor(self, yout):
        self.yout = yout

    # disponibiliza o sinal de controle
    def get_uk(self):
        return self.uk

    # Calcula o sinal de controle
    def calc_uk(self):
        self.ek = self.r - self.yout
        self.uk = self.uk1 + 0.2165*self.ek-0.2087*self.ek1
        self.ek1 = self.ek
        self.uk1 = self.uk
        self.k = self.k+1
