
from vpython import *
import numpy as np

s = 'Grafico'
grafico = graph(title = s, xtitle = 'tempo (s)', fast = True, width = 800)
curva = gcurve(color=color.blue , width = 4 , markers=False, label='Curva')

mesa = box(pos = vec(0,0,-0.15), size = vec(3,2,0.3),color = color.white)
apoio = box(pos = vec(1.35,0,0.15),size = vec(0.3, 2,0.5), color = color.cyan)

massa = box(pos = vec(0,0,0.25), size = vec(0.5,2.0,0.5), color = color.green)
mola = helix(pos = apoio.pos,axis = massa.pos-apoio.pos,
            radius = 0.2, coils = 10, color = color.green)

m = 0.2
b = 0.2
k = 1.2
Ts = 0.1


def MMA(x):                             # Define o nome da função que modela o sistema;
  x1, x2 = x                            # Variáveis de estado a partir do vetor de estados;
  dx1 = x2                              # Função de estado dx1 = f(x,u)
  dx2 = -(k/m)*x1 - (b/m)*x2 +(1/m)*0   # Função de estado dx2 = f(x,u)
    
  dx = np.array([dx1, dx2])             # Derivada do vetor de estados
    
  xn = x + Ts*dx                        # Integração
  return xn                             # Retorna a derivada do vetor de estados

t = 0.0
x = np.array([0.2, 0])
while (t<15.0):
    sleep(Ts)
    print(x)
    x = MMA(x) 
    t = t + Ts
    massa.pos = vec(x[0],0,0.25)
    mola.axis = (massa.pos - apoio.pos)
    curva.plot(t,x[0])