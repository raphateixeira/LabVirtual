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
from aeropendulo import (Graficos, AnimacaoAeropendulo,
                         Interface, ModeloMatAeropendulo)

# Instanciando um objeto AeropenduloAaeropendulo = Aeropendulo()
animacao_aeropendulo = AnimacaoAeropendulo()

# Instanciando um objeto Interface
interface = Interface(animacao_aeropendulo)

# Instanciando um objeto para plotagem dos gráficos dinâmicos dos
# estados do Aeropêndulo
g = Graficos()
graf, plot1, plot2 = g.graficos()

# Instânciando um objeto para solução matemática do sistema Aeropêndulo.
mma = ModeloMatAeropendulo()

ts = 1e-2
# Condições Iniciais dos estados
# x = [0.0, -0.5]
x = [0.0, 0.0]
t = 0.0
t_ant = 0.0

# salvando as condições iniciais dos axis pos do aeropêndulo
axis_init = animacao_aeropendulo.aeropendulo.axis
pos_init = animacao_aeropendulo.aeropendulo.pos


while True:
    vp.rate(70)
    if interface.EXE:
        dx = mma.modelo_aeropendulo(x, t)
        dt = t - t_ant
        # Atualização dos estados
        x = x + dt * dx
        print(x[1])
        t_ant = t
        t += ts
        animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                angle=x[1]*ts,
                                                origin=vp.vec(0, 5.2, 0))
        plot1.plot(t, x[0])
        plot2.plot(t, x[1])
