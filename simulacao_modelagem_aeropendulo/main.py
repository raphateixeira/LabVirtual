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
from graficos_aeropendulo import Graficos
from animacao_aeropendulo import AnimacaoAeropendulo
from modelo_mat_aeropendulo import ModeloMatAeropendulo

# Instanciando um objeto AeropenduloAaeropendulo = Aeropendulo()
animacao_aeropendulo = AnimacaoAeropendulo()

# ############# INICIO SESSÃO - TESTE MUNU INTERATIVO ##############
animacao_aeropendulo.scene.append_to_caption("\tMenu Interativo Aeropêndulo\n")
animacao_aeropendulo.scene.append_to_caption("\tRefazer Simulação\n\n")


def Reset():
    global x, t, t_ant
    g.reset()
    y = animacao_aeropendulo.aeropendulo.axis.y
    # y1 = animacao_aeropendulo.aeropendulo.pos.y
    animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                            angle=-0.5 - y,
                                            origin=vp.vec(0, 5.2, 0))
    animacao_aeropendulo.aeropendulo.axis = axis_init
    animacao_aeropendulo.aeropendulo.pos = pos_init
    # Reiniciar simulação
    x = [0.0, -0.5]
    t = 0.0
    t_ant = 0.0


animacao_aeropendulo.scene.append_to_caption("\t ")
vp.button(bind=Reset, text="Reset",
          color=vp.color.white,
          background=vp.color.red)
animacao_aeropendulo.scene.append_to_caption("\n\n\n")

# ############# FIM SESSÃO - TESTE MUNU INTERATIVO ##############

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

# salvando as condições iniciais dos axis pos do aeropêndulo
axis_init = animacao_aeropendulo.aeropendulo.axis
pos_init = animacao_aeropendulo.aeropendulo.pos


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
