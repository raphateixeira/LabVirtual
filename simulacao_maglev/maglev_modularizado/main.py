# Bibliotecas
import time

import numpy as np
from scipy.integrate import solve_ivp
from vpython import *

# Importando o Modelo Matemático do Maglev
from modelo_maglev import Maglev

# Importando o Compensador
from compensador import Compensador

# Importando Simulador e Gráfico
from animacao import Simulacao
from grafico import Grafico


# %% Criação dos objetos da planta e controlador para simular
mag = Maglev(m=29e-3, k=9.55e-6, mu=2.19e-3, I0=1)
comp = Compensador(mag, [-3*mag.lamda]*3, [-8*mag.lamda]*2)

# Criando um Objeto Simulacao
sim = Simulacao(mag_x0=mag.x0)

grafico = Grafico()


# %% Definindo os sinais de referência para rastreamento
def ref_seno(t):
    return (mag.x0*np.sin(2*pi*t))


def ref_quad(t):
    return (mag.x0)*(np.sin(2*pi*t) >= 0)


# %% Função para ajustar coordenadas do modelo às coordenadas do VPython
def converte_posicao(y_maglev):
    return (sim.bobina_3.pos + vec(0, -y_maglev, 0))*4


# %% Função para implementar ruído gaussiano
def ruido(amp):
    return amp*np.random.normal(loc=0, scale=amp)


# %% LOOP ------------------------------------------------------------------------------
# %% Criando o loop da simulação
while True:
    rate(sim.fps)
    # %% Verificação da posição do cilindro antes de executar o programa
    if sim.cil.pos == vector(12e-2, -3.5e-2, 0):
        grafico.legenda_1.text = "<b>O cilindro está na posição inicial!</b>"
        grafico.legenda_1.color = color.green
    elif sim.cil.pos == vector(0, 0, 0):
        grafico.legenda_1.text = "<b>Cilindo grudado!</b>"
        grafico.legenda_1.color = color.red
    elif sim.cil.pos.y <= 0 and sim.cil.pos.y >= -0.08 and sim.cil.pos.x == 0:
        grafico.legenda_1.text = "<b>O cilindro está na região de equilíbrio!</b>"
        grafico.legenda_1.color = color.cyan
    else:
        grafico.legenda_1.text = "<b>O cilindro está fora da região de equilíbrio!</b>"
        grafico.legenda_1.color = color.purple

    # Acionando o botão executar
    if sim.executar:
        # %% O primeiro caso: se o cilindro está na posição inicial o programa não vai sair da tela inicial.
        if sim.cil.pos == vector(12e-2, -3.5e-2, 0):
            sim.cil.pos = vector(12e-2, -3.5e-2, 0)
            grafico.yplot.delete()
            grafico.rplot.delete()
            sim.t = 0
            # time.sleep(2)
            sim.executar = not sim.executar
            sim.bt1_exe.text = "Executar"

        #  O segundo caso: o cilindro está grudado no eletroimã,
        # tem que aguardar o programa voltar pra tela inicial.
        elif sim.cil.pos == vector(0, 0, 0):
            time.sleep(3)
            sim.executar = not sim.executar
            sim.bt1_exe.text = "Executar"
            sim.cil.pos = vector(12e-2, -3.5e-2, 0)

        # O terceiro caso: o cilindro está na região 
        # de equilíbrio, logo o programa irá rodar normalmente.
        elif sim.cil.pos.y <= 0 and sim.cil.pos.y >= -0.08 and sim.cil.pos.x == 0:

            # Atualiza o sinal de referência para enviar para o solver
            match sim.M.index:
                case 0 | None:
                    def sinal(t): return ref_seno(sim.sl.value*sim.t)*(sim.sl2.value)
                case 1:
                    def sinal(t): return ref_quad(sim.sl.value*sim.t)*(sim.sl2.value)

            # Chama o solver para atualizar os estados do maglev
            sol = solve_ivp(Maglev.estadosmf, t_span=[
                            sim.t, sim.t+sim.dt], y0=sim.y,
                            args=(sinal, mag, comp))

            # Recupera os resultados da simulação
            sim.y = sol.y[:, -1]+ruido(1e-6)

            # Atualiza os gráficos
            grafico.yplot.plot(sim.t, sim.y[0])
            grafico.rplot.plot(sim.t, sinal(sim.t)+mag.x0)
            # print(y[0])

            # Atualiza a posição do cilindro
            sim.cil.pos = converte_posicao(sim.y[0])

            # Atualiza o tempo
            sim.t += sim.dt
# %% O quarto caso: o cilindro está fora da região de equilíbrio, logo ele irá cair na mesa e retornar a posição inicial.
        else:
            while sim.cil.pos.y >= -3.5e-2:
                rate(sim.fps)
                sim.cil.v = sim.cil.v+sim.g*sim.dt
                sim.cil.pos = sim.cil.pos+sim.cil.v*sim.dt
                sim.t = sim.t+sim.dt
            grafico.legenda_1.text = "<b>Aguarde o cilindro retonar a posição incial!</b>"
            grafico.legenda_1.color = color.red
            time.sleep(4)
            sim.cil.pos = vector(12e-2, -3.5e-2, 0)
            print(sim.t)
