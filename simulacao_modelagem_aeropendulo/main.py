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
import numpy as np
from aeropendulo import (Graficos, AnimacaoAeropendulo,
                         Interface, ModeloMatAeropendulo,
                         ControladorDiscreto)

# Instanciando um objeto AeropenduloAaeropendulo = Aeropendulo()
animacao_aeropendulo = AnimacaoAeropendulo()

# Instanciando um objeto Interface
interface = Interface(animacao_aeropendulo)

# Instanciando um objeto para plotagem dos gráficos dinâmicos dos
# estados do Aeropêndulo
g = Graficos()
graf, plot1, plot2, plot3, plot4 = g.graficos()

# Instânciando um objeto para solução matemática do sistema Aeropêndulo.
mma = ModeloMatAeropendulo()

# Instânciando um objeto ControladorDiscreto
controlador = ControladorDiscreto(referencia=np.pi/3.)  # np.pi/2.
u = 0  # Sinal de controle inicial

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
    vp.rate(100)
    if interface.EXE:
        dx = mma.modelo_aeropendulo(x, t)
        dt = t - t_ant
        # Atualização dos estados
        x = x + dt * dx

        controlador.set_sensor(x[1])
        controlador.calc_uk()
        u = controlador.get_uk()

        # Sinal de controle aplicado
        mma.set_u(u)
        # mma.set_u(1)

        print(x[1]*(180/np.pi))
        t_ant = t
        t += ts
        animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                angle=x[0]*ts,
                                                origin=vp.vec(0, 5.2, 0))
        plot1.plot(t, x[1])
        plot2.plot(t, x[0])
        plot3.plot(t, u)
        plot4.plot(t, controlador.r)
