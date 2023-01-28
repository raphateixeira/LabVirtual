import control as ct
import numpy as np
from scipy.integrate import solve_ivp
from vpython import *


# @title Classe Maglev
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

# Classe compensador


class Compensador:
    def __init__(self, planta, P, Q):

        # Ordem do sistema
        n = planta.A.shape[0]

        # Projeto numérico do regulador integral
        Aa = np.block([[planta.A, np.zeros((n, 1))], [-planta.C, 0]])
        Ba = np.block([[planta.B], [0]])
        Ka = ct.acker(Aa, Ba, P)
        K = Ka[:, :n]
        Ki = Ka[:, n]

        # Projeto numérico do observador
        L = ct.acker(planta.A.T, planta.C.T, Q).T

        # Matrizes para implementação do compensador
        Ar = np.block(
            [[planta.A-planta.B@K-L@planta.C, -planta.B*Ki], [np.zeros((1, n+1))]])
        Br = np.block([[L, np.zeros((n, 1))], [-1, 1]])

        # Armazena atributos do objeto
        self.Ar = Ar
        self.Br = Br
        self.K = K[0, :]
        self.Ki = Ki
        self.Ka = Ka[0, :]
        self.L = L

# -----------------------------------------------------------------


# Cria objetos da planta e controlador para simular
mag = Maglev(m=29e-3, k=9.55e-6, mu=2.19e-3, I0=1)
comp = Compensador(mag, [-3*mag.lamda]*3, [-8*mag.lamda]*2)

# Sinal de referência para rastreamento


def ref_seno(t):
    return (mag.x0*np.sin(2*pi*t))


def ref_quad(t):
    return (mag.x0)*(np.sin(2*pi*t) >= 0)


# Equações de estados em malha fechada


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

# Função para ajustar coordenadas do modelo às coordenadas do VPython


def converte_posicao(y_maglev):
    return (bobina.pos + vec(0, -y_maglev, 0))*4

# Função para implementar ruído gaussiano


def ruido(amp):
    return amp*np.random.normal(loc=0, scale=amp)

# Simulação e animação


executar = False
reset = False


def acionar_btn(b):
    global executar
    if executar:
        b.text = "Executar"
    else:
        b.text = "Pausar"
    executar = not executar


def acionar_btn2(c):
    global reset
    if reset:
        c.text = "Resetar"
    else:
        c.text = "Resetado"


# Dimensões da cena
scene = canvas(width=600, height=445, align='left',
               title='<b>SIMULAÇÃO MAGLEV V1.0<b>\n\n')

# Criação da mesa, suporte e eletroimã
mesa = box(pos=vec(5e-2, -9.5e-2, 0), size=vec(20e-2,
           1e-2, 10e-2), color=vec(0.359, 0.097, 0))

sup5 = cylinder(pos=vec(10e-2, -9.5e-2, 0), size=vector(18e-2,
                                                        0.8e-2, 0.8e-2), color=vec(0.618, 0.668, 0.636), axis=vec(0, 1, 0))

cnx2 = sphere(pos=vec(9.9e-2, 8e-2, 0), radius=1e-2,
              color=vec(0.618, 0.668, 0.636))

sup4 = cylinder(pos=vec(0, 8.5e-2, 0), size=vector(10e-2, 0.8e-2,
                                                   0.8e-2), color=vec(0.618, 0.668, 0.636), axis=vec(0, 0, 0))

cnx1 = sphere(pos=vec(0, 8e-2, 0), radius=1e-2, color=vec(0.618, 0.668, 0.636))

sup3 = cylinder(pos=vec(0, 5e-2, 0), size=vector(3e-2, 0.8e-2,
                                                 0.8e-2), color=vec(0.618, 0.668, 0.636), axis=vec(0, 1, 0))

bobina2 = cylinder(pos=vec(0, 4.5e-2, 0), size=vector(0.5e-2,
                   6e-2, 6e-2), color=vec(0.0, 0.568, 0.864), axis=vec(0, 1, 0))

bobina1 = cylinder(pos=vec(0, 0.5e-2, 0), size=vector(4e-2,
                   4e-2, 4e-2), color=vec(1.0, 0.387, 0.0), axis=vec(0, 1, 0))

# L_bobina = 10e-2
# r_bobina = 1e-2
bobina = cylinder(pos=vec(0, 0, 0), size=vector(
    0.5e-2, 6e-2, 6e-2), color=vec(0.0, 0.568, 0.864), axis=vec(0, 1, 0))

# Cria o cilindro flutuante
L_cilindro = 5e-2
r_cilindro = 1e-2
cil = cylinder(pos=converte_posicao(mag.x0), axis=vec(
    0, -L_cilindro, 0), color=vec(0.902, 0.827, 0), radius=r_cilindro)

# Parâmetros de simulação
fps = 50                           # Taxa de quadros
dt = 1/fps                         # Intervalo de tempo real de atualização
t = 0                              # Armazena tempo, tempo inicial
y = [mag.x0*1.05, 0, 0, 0, 0]      # Estado, estado inicial


# slider e container: controles em tempo real (teste)

# Criando o botão executar
scene.append_to_title('<b>Controles Básicos:</b>\n\n')
button(pos=scene.title_anchor, text="Executar", bind=acionar_btn)

button(pos=scene.title_anchor, text="Resetar", bind=acionar_btn2)
scene.append_to_title('\n\n')


# Função para mostrar o valor de frequência e da amplitude ajustado pelo slider


def setfreq(s):
    wt.text = '{:1.2f}'.format(s.value)


def setAmp(a):
    ampl.text = '{:1.2f}'.format(a.value)


scene.append_to_title('<b>Frequência do Sinal:<b>')

# Slider para controlar a frequência do sinal de referência senoidal
sl = slider(pos=scene.title_anchor, min=0.1, max=4,
            value=1., length=220, right=15, bind=setfreq)
# Caixa de texto para mostrar o valor real da frequência
wt = wtext(pos=scene.title_anchor, text='{:1.2f}'.format(sl.value))
scene.append_to_title('')

scene.append_to_title('    <b>Amplitude do Sinal:<b>')

# Slider para controlar a amplitude do sinal de referência senoidal
sl2 = slider(pos=scene.title_anchor, min=0.1, max=1,
             value=.1, length=220, right=15, bind=setAmp)
# Caixa de texto para mostrar o valor real da frequência
ampl = wtext(pos=scene.title_anchor, text='{:1.2f}'.format(sl2.value))
scene.append_to_title('\n\n')


# Cria menu e associa função evento

scene.append_to_title('<b>Sinal de Referência:</b>\n\n')


def Menu(m):
    print('ok')


M = menu(pos=scene.title_anchor, choices=[
         'Onda Senoidal', 'Onda Quadrada'], bind=Menu)
scene.append_to_title('\n\n')


# Gráficos para mostrar sinais
grafico = graph(width=700, height=400, align='left', title='Resposta do sistema a um sinal de referência', xtitle='Tempo (s)',
                ytitle='Posição (mm)', fast=False)
# Curva da posição real
yplot = gdots(color=color.red, size=2, label='Sistema')
# Curva do sinal de referência
rplot = gcurve(color=color.blue, label='Referência')

restart = True

# Loop infinito
while True:
    rate(fps)

    if executar:

        # Atualiza o sinal de referência para enviar para o solver
        match M.index:
            case 0 | None:
                def sinal(t): return ref_seno(sl.value*t)*(sl2.value)
            case 1:
                def sinal(t): return ref_quad(sl.value*t)*(sl2.value)

        # Chama o solver para atualizar os estados do maglev
        sol = solve_ivp(estadosmf, t_span=[
                        t, t+dt], y0=y, args=(sinal, mag, comp))

        # Recupera os resultados da simulação
        y = sol.y[:, -1]+ruido(1e-6)

        # Atualiza os gráficos
        yplot.plot(t, y[0])
        rplot.plot(t, sinal(t)+mag.x0)
        # print(y[0])

        # Atualiza a posição do cilindro
        cil.pos = converte_posicao(y[0])

        # Atualiza o tempo
        t += dt
