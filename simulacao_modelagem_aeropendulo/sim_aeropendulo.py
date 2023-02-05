# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# ----------------------------------------------------
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Tema: Simulação Aeropêndulo
# Autor: Oséias Farias
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
# ----------------------------------------------------


import vpython as vp
from graficos_aeropendulo import graficos

# Parâmetros do Aeropêndulo
comprimento_braco = 4.4

scene = vp.canvas(title="<center><h1>Aeropêndulo</h1><center/>", width=650,
                  height=580, align="left", autoscale=0, range=5,
                  center=vp.vec(0, 3, 0),
                  background=vp.vector(1.7, 0.7, 0.9),
                  color=vp.vec(1, 0.6, 0.6),
                  forward=vp.vec(-0.3, 0, -1))

# Ambiente de sinulação.
base = vp.box(pos=vp.vec(0, -0.85, 0), size=vp.vec(30, 0.2, 15),
              texture=vp.textures.wood)
parede = vp.box(pos=vp.vec(0, 7.1, -7.55), size=vp.vec(30, 16, 0.2),
                color=vp.vec(0.1, 0.1, 0.1), shininess=0.05)
sitio = vp.text(pos=vp.vec(0, 8.1, -7.45), text="AEROPÊNDULO",
                color=vp.vec(1, 0.6, 0.6), align='center', depth=0)

# Braço do Aeropêndulo.
barra = vp.box(pos=vp.vec(0, -1.4, 0),
               size=vp.vec(0.2, comprimento_braco, 0.2),
               color=vp.vec(0.5, 0.5, 0.95))

# Base que acopla o motor ao braço.
base_motor = vp.cylinder(pos=vp.vec(-0.2, -4, 0), radius=0.4,
                         axis=vp.vec(0.4, 0, 0),
                         color=vp.vec(0.5, 0.5, 0.95))
# Armadura do motor.
base2_motor = vp.box(pos=vp.vec(-0.4, -4, 0), size=vp.vec(0.4, 0.4, 0.4),
                     color=vp.vec(1, 1, 0))

# Eixo que da hélice do motor.
base_helice = vp.cylinder(pos=vp.vec(-0.8, -4, 0), radius=0.05,
                          axis=vp.vec(0.4, 0, 0),
                          color=vp.vec(0.5, 0.5, 0.8))

# Hélice.
helice = vp.box(pos=vp.vec(-0.8, -4, 0), size=vp.vec(0.05, 0.2, 2),
                color=vp.vec(1, 1, 0))

# Motor completo.
motor = vp.compound([base_motor, base2_motor, base_helice])

# Motor + Hélice.
motor_helice = vp.compound([motor, helice])

# Aeropêndulo
pendulo = vp.compound([barra, motor_helice])
pendulo.pos = vp.vec(-0.31, 2.7, 0)

# Eixo de sustentação.
eixo = vp.cylinder(pos=vp.vec(0, 5.2, 0.3), radius=0.09,
                   axis=vp.vec(0, 0, -2),
                   color=vp.vec(0.7, 0.4, 0.1))

# Estrutura de sustentação do aeropêndulo.
b1 = vp.box(pos=vp.vec(0, 1.7, -2), size=vp.vec(3, 8, 0.6),
            dcolor=vp.vec(0.8, 0.8, 0.8))
b2 = vp.box(pos=vp.vec(0, -0.6, -1.5), size=vp.vec(4.5, 0.4, 2.5),
            color=vp.vec(0.8, 0.8, 0.8))
logo = vp.box(pos=vp.vec(0, 2.5, -1.7),
              texture="./utils/logoufpa.png", size=vp.vec(2, 2, 0.2))
ufpa = vp.text(pos=vp.vec(0, 3.7, -1.7), text="UFPA",
               color=vp.vec(1, 0.6, 0.6), height=0.5,
               align='center', depth=0)

graf, plot1, plot2, plot3 = graficos()

pendulo.w = 10
pendulo.angulo = 0
pendulo.l = 3
dt = 0.01
t = 0

while True:
    vp.rate(20)
    t += dt
    pendulo.a = -98*vp.sin(pendulo.angulo)/pendulo.l
    pendulo.w = pendulo.w + pendulo.a*dt
    pendulo.angulo = pendulo.angulo + pendulo.w*dt
    pendulo.rotate(axis=vp.vec(0, 0, 1), angle=pendulo.w*dt,
                   origin=vp.vec(0, 5.2, 0))
    plot1.plot(t, pendulo.a)
    plot2.plot(t, pendulo.w)
    plot3.plot(t, pendulo.angulo)
