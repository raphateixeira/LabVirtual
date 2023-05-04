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

# Instanciando um objeto AeropenduloAaeropendulo()
animacao_aeropendulo = AnimacaoAeropendulo()

# Instanciando um objeto para plotagem dos gráficos dinâmicos dos
# estados do Aeropêndulo
g = Graficos()
graf, plot1, plot2, plot3, plot4 = g.graficos()

# Instânciando um objeto para solução matemática do sistema Aeropêndulo.
Km = 0.0296
m = 0.36
d = 0.03
J = 0.0106
c = 0.0076
mma = ModeloMatAeropendulo(K_m=Km, m=m, d=d, J=J, c=c)

# Instânciando um objeto ControladorDiscreto
controlador = ControladorDiscreto(referencia=0.01)
u = 0  # Sinal de controle inicial

# Instanciando um objeto Interface
interface = Interface(animacao_aeropendulo, controlador)

ts = 1e-2
# Condições Iniciais dos estados
x = np.array([0.0, 0.0])
t = 0.0
t_ant = 0.0

# Simulação do Sistema
while True:
    vp.rate(100)
    if interface.EXE:
        # Calcula as derivadas do sitema
        dx = mma.modelo_aeropendulo(x, t)
        dt = t - t_ant

        # Atualização dos estados
        x = x + dt * dx

        # Pega o Ângulo e envia para o controlador (Realimentação do sistema)
        controlador.set_sensor(x[1])

        # O controlador calcula o sinal de controle
        controlador.control_pi()

        # Controle proporcional
        # controlador.controle_proporcional(kp=10.0)
        # pega o sinal de controle calculado e salva na variável u
        u = controlador.get_u()

        # Sinal de controle aplicado a entrada do sistema
        mma.set_u(u)

        # print(x[1]*(180/np.pi))
        t_ant = t
        t += ts

        # Atualiza o ângulo do Aeropêndulo
        animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                angle=x[0]*ts,
                                                origin=vp.vec(0, 5.2, 0))

        # Animação da dinâmica da Hélice
        animacao_aeropendulo.update_helice(x[0], ts)

        print(x[1] + interface.valor_angle)
        # Gráfico do ângulo.
        plot1.plot(t, x[1] + interface.valor_angle)
        # Gráfico do sinal de referência
        plot2.plot(t, controlador.r + interface.valor_angle)
        # Gráfico da velocidade ângular.
        plot3.plot(t, x[0])
        # Gráfico do sinal de controle
        plot4.plot(t, u)
