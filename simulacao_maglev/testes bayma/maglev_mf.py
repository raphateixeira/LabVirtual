from vpython import *
import numpy as np
import control as ct
from scipy.integrate import solve_ivp

#@title Classe Maglev
class Maglev:
  def __init__(self,m,k,mu,I0):
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
    self.A = np.array([[0,1.],[self.lamda**2,0]])
    self.B = np.array([[0],[-self.a]])
    self.C = np.array([[1.,0]])

## Classe compensador
class Compensador:
  def __init__(self, planta, P, Q):
    
    n = planta.A.shape[0]

    Aa = np.block([[planta.A,np.zeros((n,1))],[-planta.C,0]])
    Ba = np.block([[planta.B],[0]])
    Ka = ct.acker(Aa,Ba,P)
    K = Ka[:,:n]
    Ki = Ka[:,n]

    L = ct.acker(planta.A.T,planta.C.T,Q).T

    Ar = np.block([[planta.A-planta.B@K-L@planta.C, -planta.B*Ki],[np.zeros((1,n+1))]])
    Br = np.block([[L,np.zeros((n,1))],[-1,1]])

    self.Ar = Ar
    self.Br = Br
    self.K = K[0,:]
    self.Ki = Ki
    self.Ka = Ka[0,:]
    self.L = L
    self.estados = [0]*(n+1)

mag = Maglev(m=29e-3, k=9.55e-6, mu=2.19e-3, I0=1)
comp = Compensador(mag, [-3*mag.lamda]*3,[-8*mag.lamda]*2)

## Sinal de referência para rastreamento
def ref(t):
    return (0.1*mag.x0*np.sin(2*pi*t))

## Sistema em espaço de estados em malha fechada
def estadosmf(t,x,ref,planta,comp):
  # Separa os estados do controlador
  z = x[2:]
  # Lista que vai conter os resultados
  ddt = [0.]*5
  # Corrente do imã - corrente de equilíbrio + correção do controlador
  I = planta.I0 - comp.Ka@z
  # Variação de posição em relação ao equilíbrio - precisa para o observador
  Dx1 = x[0]-planta.x0
  # Vetor contendo os sinais de entrada do controle, saída + referência
  u =[Dx1, ref(t)]
  # Planta:
  ddt[0] = x[1]
  ddt[1] = planta.g - planta.k*I**2/(planta.m*(x[0]+planta.mu)**2)
  # Controlador:
  ddt[2:] = comp.Ar@z + comp.Br@u
  return ddt

## Simulação e animação
scene.width = 600
scene.height = 600

L_bobina = 10e-2
r_bobina = 1e-2
bobina = cylinder(pos = vec(0,0,0), color = color.blue, radius = r_bobina, axis = vec(0,L_bobina,0))

def converte_posicao(y_maglev):
  return bobina.pos + vec(0,-y_maglev,0)

def ruido(amp):
  return amp*np.random.normal(loc=0,scale=amp)

L_cilindro = 5e-2
r_cilindro = 1e-2
cil = cylinder(pos = converte_posicao(mag.x0), axis = vec(0,-L_cilindro,0), radius = r_cilindro)

fps = 50
dt = 1/fps
t = 0
y = [mag.x0*1.05, 0, 0, 0, 0]


def setfreq(s):
    wt.text = '{:1.2f}'.format(s.value)

scene.append_to_caption('\n\n')
sl = slider(pos=scene.caption_anchor, min=0.1, max=4, value=1., length=220, right=15, bind=setfreq)
wt = wtext(text='{:1.2f}'.format(sl.value))
scene.append_to_caption('\n\n')

yplot = gcurve(color=color.red)
rplot = gcurve(color=color.blue)

while True:
    rate(fps)
    sinal = lambda t: ref(sl.value*t)
    sol = solve_ivp(estadosmf,t_span=[t,t+dt],y0=y, args=(sinal,mag,comp))
    y = sol.y[:,-1]+ruido(1e-6)
    yplot.plot(t,y[0])
    rplot.plot(t,sinal(t)+mag.x0)
    #print(y[0])
    cil.pos = converte_posicao(y[0])
    t += dt

