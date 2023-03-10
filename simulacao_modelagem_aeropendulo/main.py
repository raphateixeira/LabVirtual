# ----------------------------------------------------
# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# ----------------------------------------------------
#
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Tema: Simulação Aeropêndulo
# Autor: Oséias Farias
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
#  ----------------------------------------------------
#
import vpython as vp
from graficos_aeropendulo import Graficos
from animacao_aeropendulo import AnimacaoAeropendulo
from modelo_mat_aeropendulo import ModeloMatAeropendulo

# Instanciando um objeto AeropenduloAaeropendulo = Aeropendulo()
animacao_aeropendulo = AnimacaoAeropendulo()

# Instanciando um objeto para plotagem dos gráficos dinâmicos dos
# estados do Aeropêndulo
g = Graficos()
graf, plot1, plot2 = g.graficos()

# Instânciando um objeto para solução matemática do sistema Aeropêndulo.
mma = ModeloMatAeropendulo()

ts = 1e-2
# Condições Iniciais dos estados
x = [0.0, -0.5]
t = 0.0
t_ant = 0.0

while True:
    vp.rate(70)
    dx = mma.modelo_aeropendulo(x, t)
    dt = t - t_ant
    x = x + dt * dx

    t_ant = t
    t += ts
    animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                            angle=x[1]*ts,
                                            origin=vp.vec(0, 5.2, 0))
    plot1.plot(t, x[0])
    plot2.plot(t, x[1])
