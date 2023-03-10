# %% Bibliotecas
import time

import control as ct
import numpy as np
from scipy.integrate import solve_ivp
from vpython import *


# %% MODELAGEM ------------------------------------------------------------------------------
# %% Modelagem da Planta do MAGLEV
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

# %% Projeto do Compensador


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


# %% Criação dos objetos da planta e controlador para simular
mag = Maglev(m=29e-3, k=9.55e-6, mu=2.19e-3, I0=1)

comp = Compensador(mag, [-3*mag.lamda]*3, [-8*mag.lamda]*2)

# %% Definindo os sinais de referência para rastreamento


def ref_seno(t):
    return (mag.x0*np.sin(2*pi*t))


def ref_quad(t):
    return (mag.x0)*(np.sin(2*pi*t) >= 0)

# %% Equações de estados em malha fechada


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

# %% Função para ajustar coordenadas do modelo às coordenadas do VPython


def converte_posicao(y_maglev):
    return (bobina_3.pos + vec(0, -y_maglev, 0))*4

# %% Função para implementar ruído gaussiano


def ruido(amp):
    return amp*np.random.normal(loc=0, scale=amp)


# %% SIMULAÇÃO ------------------------------------------------------------------------------
# %% Criação da função do botão executar
executar = False


def acionar_btn(b):
    global executar
    if executar:
        b.text = "Executar"
    else:
        b.text = "Pausar"
    executar = not executar

# %% Criando o Grid na animação


class Grid:
    def __init__(self):
        self.pts = []
        self.pts.append(sphere(pos=vector(0, 0, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.01, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.02, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.03, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.0144154, 0),
                               radius=0.1e-2, color=color.red))

        self.pts.append(sphere(pos=vector(0, -0.04, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.05, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.06, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.07, 0),
                               radius=0.1e-2, color=color.black))

        self.pts.append(sphere(pos=vector(0, -0.08, 0),
                               radius=0.1e-2, color=color.black))

    def visible(self, vis):
        for s in self.pts:
            s.visible = vis


# %% Criando a cena e definindo seus parâmetros
scene = canvas(width=700, height=445, align='left',
               title='<b>SIMULAÇÃO MAGLEV V1.0<b>\n\n')
scene.background = color.white
scene.foreground = color.black
scene.userspin = False
constrain = False
grid = None
drag = False

# %% Criando o desenho da animação
mesa = box(pos=vec(5e-2, -9e-2, 0), size=vec(20e-2, 1e-2, 10e-2),
           color=vec(0.570, 0.259, 0.103))

suporte_1 = cylinder(pos=vec(14e-2, -8.5e-2, 0), size=vector(17e-2,
                     0.8e-2, 0.8e-2), color=vec(0.618, 0.668, 0.636), axis=vec(0, 1, 0))

conexao_1 = sphere(pos=vec(14e-2, 8e-2, 0), radius=1e-2,
                   color=vec(0.618, 0.668, 0.636))

suporte_2 = cylinder(pos=vec(0, 8e-2, 0), size=vec(14e-2, 0.8e-2,
                     0.8e-2), color=vec(0.618, 0.668, 0.636), axis=vec(0, 0, 0))

conexao_2 = sphere(pos=vec(0, 8e-2, 0), radius=1e-2,
                   color=vec(0.618, 0.668, 0.636))

suporte_3 = cylinder(pos=vec(0, 5e-2, 0), size=vector(3e-2, 0.8e-2,
                                                      0.8e-2), color=vec(0.618, 0.668, 0.636), axis=vec(0, 1, 0))

bobina_1 = cylinder(pos=vec(0, 4.5e-2, 0), size=vector(0.5e-2,
                                                       6e-2, 6e-2), color=vec(0.0, 0.568, 0.864), axis=vec(0, 1, 0))

bobina_2 = cylinder(pos=vec(0, 0.5e-2, 0), size=vector(4e-2,
                                                       4e-2, 4e-2), color=vec(1.0, 0.387, 0.0), axis=vec(0, 1, 0))

bobina_3 = cylinder(pos=vec(0, 0, 0), size=vector(
    0.5e-2, 6e-2, 6e-2), color=vec(0.0, 0.568, 0.864), axis=vec(0, 1, 0))

# Cria o cilindro flutuante
L_cilindro = 5e-2
r_cilindro = 1e-2
cil = cylinder(pos=vec(12e-2, -3.5e-2, 0), axis=vec(0, -L_cilindro,
               0), color=vec(0.902, 0.827, 0), radius=r_cilindro, velocity=vector(0, 0, 0))

# %% Definindo as funções de interação do usuário


def down():
    global drag
    if constrain:
        pos = vector(round(cil.pos.x, 2), round(
            cil.pos.y, 2), round(cil.pos.z, 2))
    drag = True


def move():
    global drag
    if drag:
        cil.pos = scene.mouse.pos


def up():
    global drag, ff
    if constrain:
        cil.pos = vector(round(cil.pos.x, 2), round(
            cil.pos.y, 2), round(cil.pos.z, 2))
    drag = False
    print(cil.pos, "\n")


scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)

# %% Criando as funções de ativação do GRID e constrição de movimento


def setgrid(evt):
    global grid
    if evt.checked:
        if not grid:
            grid = Grid()
        else:
            grid.visible(True)
    else:
        grid.visible(False)


def setconstrain(evt):
    global constrain
    constrain = evt.checked


# %% Parâmetros de simulação
fps = 50                           # Taxa de quadros
dt = 1/fps                         # Intervalo de tempo real de atualização
t = 0                              # Armazena tempo, tempo inicial
y = [mag.x0*1.05, 0, 0, 0, 0]      # Estado, estado inicial

# %% Criando o menu interativo
# Título
scene.append_to_title('<b>CONTROLES BÁSICOS:</b>\n\n')
# Botão Executar
bt1_exe = button(pos=scene.title_anchor, text="Executar", bind=acionar_btn)
scene.append_to_title('   ')
# Checkbox do GRID
checkbox(pos=scene.title_anchor, bind=setgrid)
scene.append_to_title('<b>Exibir região de equilíbrio</b>')
scene.append_to_title('   ')
# Checkbox da constrição de movimento
checkbox(pos=scene.title_anchor, bind=setconstrain)
scene.append_to_title('<b>Constrição de movimento</b>')
scene.append_to_title('\n\n')

# %% Criando a função para mostrar o valor de frequência e da amplitude ajustado pelo slider


def setfreq(s):
    wt.text = '{:1.2f}'.format(s.value)


def setAmp(a):
    ampl.text = '{:1.2f}'.format(a.value)


# %% Criando os botões de ajuste da frequência e da amplitude
scene.append_to_title('<b>Frequência do Sinal:<b>')
# Slider para controlar a frequência do sinal de referência senoidal
sl = slider(pos=scene.title_anchor, min=0.1, max=4,
            value=1., length=220, right=15, bind=setfreq)
# Caixa de texto para mostrar o valor real da frequência
wt = wtext(pos=scene.title_anchor, text='{:1.2f}'.format(sl.value))
scene.append_to_title('')

scene.append_to_title('\n\n<b>Amplitude do Sinal:<b>')
# Slider para controlar a amplitude do sinal de referência senoidal
sl2 = slider(pos=scene.title_anchor, min=0.1, max=1,
             value=.1, length=220, right=15, bind=setAmp)
# Caixa de texto para mostrar o valor real da frequência
ampl = wtext(pos=scene.title_anchor, text='{:1.2f}'.format(sl2.value))
scene.append_to_title('\n\n')

# %% Criando o menu de escolha do sinal de referência
scene.append_to_title('<b>Sinal de Referência:</b>')
scene.append_to_title(' ')


def Menu(m):
    print('ok')


M = menu(pos=scene.title_anchor, choices=[
         'Onda Senoidal', 'Onda Quadrada'], bind=Menu)
scene.append_to_title('  ')

# %% Criando o gráfico para mostrar os sinais
grafico = graph(width=700, height=400, align='left', title='Resposta do sistema a um sinal de referência', xtitle='Tempo (s)',
                ytitle='Posição (mm)', fast=False)
# Curva da posição real
yplot = gdots(color=color.red, size=2, label='Sistema')
# Curva do sinal de referência
rplot = gcurve(color=color.blue, label='Referência')

# %% Criação da legenda flutuante

legenda_1 = label(pos=vec(
    0, 11.5e-2, 0), text="<b>O cilindro está na posição inicial!</b>", font="Verdana")

# %% Criação do controlador interativo
# Criando a função para escolher o tipo de controlador e fornecendo as matrizes


def recebe_Ar(Ar):
    new_Ar = np.asarray(Ar)
    wtext(pos=scene.title_anchor, text='\n\n<b>Recebido</b>')
    print(new_Ar)
    type(new_Ar)


def recebe_Br(Br):
    new_Ar = np.asarray(Br)
    wtext(pos=scene.title_anchor, text='\n\n<b>Recebido</b>')
    print(new_Ar)
    type(new_Ar)


def recebe_K(K):
    new_Ar = np.asarray(K)
    wtext(pos=scene.title_anchor, text='\n\n<b>Recebido</b>')
    print(new_Ar)
    type(new_Ar)


def check_action(x):
    global text_1, MM, text_2, bt_1, text_3, bt_2, text_4, bt_3, esp
    if x.checked:
        text_1 = wtext(pos=scene.title_anchor,
                       text='<b>Tipo de Controlador:</b> ')
        MM = menu(pos=scene.title_anchor, choices=[
                  'Espaço de Estados', 'Função de Transferência'], bind=Menu)
        text_2 = wtext(pos=scene.title_anchor,
                       text='\n\n<b>Matriz Ar:</b> ')
        bt_1 = winput(pos=scene.title_anchor,
                      prompt='Enter here', type='string', bind=recebe_Ar)

        text_3 = wtext(pos=scene.title_anchor,
                       text='\n\n<b>Matriz Br:</b> ')
        bt_2 = winput(pos=scene.title_anchor,
                      prompt='Enter here', type='string', bind=recebe_Br)

        text_4 = wtext(pos=scene.title_anchor,
                       text='\n\n<b>Matriz K:</b> ')
        bt_3 = winput(pos=scene.title_anchor,
                      prompt='Enter here', type='string', bind=recebe_K)
        esp = wtext(pos=scene.title_anchor, text='\n\n')

    else:
        text_1.text = ""
        MM.delete()
        text_2.text = ""
        bt_1.delete()
        text_3.text = ""
        bt_2.delete()
        text_4.text = ""
        bt_3.delete()
        esp.text = ""


# %% Criando o botão que chama o controlador interativo
scene.append_to_title('\n\n')
bt3 = checkbox(pos=scene.title_anchor,
               text='<b>CONTROLE PERSONALIZADO</b>', bind=check_action)
scene.append_to_title('\n\n')


# %% Parâmetros de simulação de queda
# Velocidade inicial do cilindro
cil.v = vector(0, 0, 0)
# Gravidade inicial do cilindro
g = vector(0, -5.8e-2, 0)
# %% LOOP ------------------------------------------------------------------------------
# %% Criando o loop da simulação
while True:
    rate(fps)
# %% Verificação da posição do cilindro antes de executar o programa
    if cil.pos == vector(12e-2, -3.5e-2, 0):
        legenda_1.text = "<b>O cilindro está na posição inicial!</b>"
        legenda_1.color = color.green
    elif cil.pos == vector(0, 0, 0):
        legenda_1.text = "<b>Cilindo grudado!</b>"
        legenda_1.color = color.red
    elif cil.pos.y <= 0 and cil.pos.y >= -0.08 and cil.pos.x == 0:
        legenda_1.text = "<b>O cilindro está na região de equilíbrio!</b>"
        legenda_1.color = color.cyan
    else:
        legenda_1.text = "<b>O cilindro está fora da região de equilíbrio!</b>"
        legenda_1.color = color.purple
# %% Acionando o botão executar
    if executar:
        # %% O primeiro caso: se o cilindro está na posição inicial o programa não vai sair da tela inicial.
        if cil.pos == vector(12e-2, -3.5e-2, 0):
            cil.pos = vector(12e-2, -3.5e-2, 0)
            yplot.delete()
            rplot.delete()
            t = 0
            # time.sleep(2)
            executar = not executar
            bt1_exe.text = "Executar"
# %% O segundo caso: o cilindro está grudado no eletroimã, tem que aguardar o programa voltar pra tela inicial.
        elif cil.pos == vector(0, 0, 0):
            time.sleep(3)
            executar = not executar
            bt1_exe.text = "Executar"
            cil.pos = vector(12e-2, -3.5e-2, 0)
# %% O terceiro caso: o cilindro está na região de equilíbrio, logo o programa irá rodar normalmente.
        elif cil.pos.y <= 0 and cil.pos.y >= -0.08 and cil.pos.x == 0:

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
# %% O quarto caso: o cilindro está fora da região de equilíbrio, logo ele irá cair na mesa e retornar a posição inicial.
        else:
            while cil.pos.y >= -3.5e-2:
                rate(fps)
                cil.v = cil.v+g*dt
                cil.pos = cil.pos+cil.v*dt
                t = t+dt
            legenda_1.text = "<b>Aguarde o cilindro retonar a posição incial!</b>"
            legenda_1.color = color.red
            time.sleep(4)
            cil.pos = vector(12e-2, -3.5e-2, 0)
            print(t)
