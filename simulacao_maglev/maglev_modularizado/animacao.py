import numpy as np
from vpython import *


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


# SIMULAÇÃO ------------------------------------------------------------------------------
class Simulacao:
    def __init__(self, mag_x0):
        self.mag_x0 = mag_x0
        self.executar = False

        #  Criando a cena e definindo seus parâmetros
        self.scene = canvas(width=600, height=445, align='left',
                            title='<b>SIMULAÇÃO MAGLEV V1.0<b>\n\n')
        self.scene.background = color.white
        self.scene.foreground = color.black
        self.scene.userspin = False
        self.constrain = False
        self.grid = None
        self.drag = False

        # definindo os parâmetros do Cilindro
        self.L_cilindro = 5e-2
        self.r_cilindro = 1e-2

        # Animação
        self.desenho_animacao()

        self.scene.bind("mousedown", self.down)
        self.scene.bind("mousemove", self.move)
        self.scene.bind("mouseup", self.up)

        self.menu_interativo()

        self.btm_freq_ampl()

        self.M = menu(pos=self.scene.title_anchor, choices=[
            'Onda Senoidal', 'Onda Quadrada'], bind=self.Menu)
        self.scene.append_to_title('  ')

        # %% Parâmetros de simulação
        self.fps = 50                           # Taxa de quadros
        self.dt = 1/self.fps                         # Intervalo de tempo real de atualização
        self.t = 0                              # Armazena tempo, tempo inicial
        self.y = [mag_x0*1.05, 0, 0, 0, 0]      # Estado, estado inicial

        self.btn_controlador_interativo()
        #  Parâmetros de simulação de queda
        # Velocidade inicial do cilindro
        self.cil.v = vector(0, 0, 0)
        # Gravidade inicial do cilindro
        self.g = vector(0, -5.8e-2, 0)

    # Criação da função do botão executar
    def acionar_btn(self, b):
        if self.executar:
            b.text = "Executar"
        else:
            b.text = "Pausar"
        self.executar = not self.executar

    def desenho_animacao(self):
        # %% Criando o desenho da animação
        self.mesa = box(pos=vec(5e-2, -9e-2, 0), size=vec(20e-2, 1e-2, 10e-2),
                        color=vec(0.570, 0.259, 0.103))

        self.suporte_1 = cylinder(pos=vec(14e-2, -8.5e-2, 0),
                                  size=vector(17e-2, 0.8e-2, 0.8e-2),
                                  color=vec(0.618, 0.668, 0.636),
                                  axis=vec(0, 1, 0))

        self.conexao_1 = sphere(pos=vec(14e-2, 8e-2, 0), radius=1e-2,
                                color=vec(0.618, 0.668, 0.636))

        self.suporte_2 = cylinder(pos=vec(0, 8e-2, 0),
                                  size=vec(14e-2, 0.8e-2, 0.8e-2),
                                  color=vec(0.618, 0.668, 0.636),
                                  axis=vec(0, 0, 0))

        self.conexao_2 = sphere(pos=vec(0, 8e-2, 0), radius=1e-2,
                        color=vec(0.618, 0.668, 0.636))

        self.suporte_3 = cylinder(pos=vec(0, 5e-2, 0),
                                  size=vector(3e-2, 0.8e-2, 0.8e-2),
                                  color=vec(0.618, 0.668, 0.636),
                                  axis=vec(0, 1, 0))

        self.bobina_1 = cylinder(pos=vec(0, 4.5e-2, 0),
                                 size=vector(0.5e-2, 6e-2, 6e-2),
                                 color=vec(0.0, 0.568, 0.864),
                                 axis=vec(0, 1, 0))

        self.bobina_2 = cylinder(pos=vec(0, 0.5e-2, 0),
                                 size=vector(4e-2, 4e-2, 4e-2),
                                 color=vec(1.0, 0.387, 0.0),
                                 axis=vec(0, 1, 0))

        self.bobina_3 = cylinder(pos=vec(0, 0, 0),
                                 size=vector(0.5e-2, 6e-2, 6e-2),
                                 color=vec(0.0, 0.568, 0.864),
                                 axis=vec(0, 1, 0))

        # Cria o cilindro flutuante
        self.cil = cylinder(pos=vec(12e-2, -3.5e-2, 0),
                            axis=vec(0, -self.L_cilindro, 0),
                            color=vec(0.902, 0.827, 0),
                            radius=self.r_cilindro,
                            velocity=vector(0, 0, 0))

    # %% Definindo as funções de interação do usuário
    # @classmethod
    def down(self):
        if self.constrain:
            self.cil.pos = vector(round(self.cil.pos.x, 2), round(
                                  self.cil.pos.y, 2), round(self.cil.pos.z, 2))
        self.drag = True

    # @classmethod
    def move(self):
        if self.drag:
            self.cil.pos = self.scene.mouse.pos

    # @classmethod
    def up(self):
        if self.constrain:
            self.cil.pos = vector(round(self.cil.pos.x, 2),
                                  round(self.cil.pos.y, 2),
                                  round(self.cil.pos.z, 2))
        self.drag = False
        print(self.cil.pos, "\n")

    # %% Criando as funções de ativação do GRID e constrição de movimento
    def setgrid(self, evt):
        if evt.checked:
            if not self.grid:
                self.grid = Grid()
            else:
                self.grid.visible(True)
        else:
            self.grid.visible(False)

    def setconstrain(self, evt):
        self.constrain = evt.checked

    # %% Criando o menu interativo
    # Título
    def menu_interativo(self):
        self.scene.append_to_title('<b>CONTROLES BÁSICOS:</b>\n\n')
        # Botão Executar
        self.bt1_exe = button(pos=self.scene.title_anchor,
                              text="Executar", bind=self.acionar_btn)
        self.scene.append_to_title('   ')
        # Checkbox do GRID
        checkbox(pos=self.scene.title_anchor, bind=self.setgrid)
        self.scene.append_to_title('<b>Exibir região de equilíbrio</b>')
        self.scene.append_to_title('   ')
        # Checkbox da constrição de movimento
        checkbox(pos=self.scene.title_anchor, bind=self.setconstrain)
        self.scene.append_to_title('<b>Constrição de movimento</b>')
        self.scene.append_to_title('\n\n')

    # Criando a função para mostrar o valor de frequência e da amplitude ajustado pelo slider

    def setfreq(self, s):
        self.wt.text = '{:1.2f}'.format(s.value)

    def setAmp(self, a):
        self.ampl.text = '{:1.2f}'.format(a.value)

    def btm_freq_ampl(self):
        # Criando os botões de ajuste da frequência e da amplitude
        self.scene.append_to_title('<b>Frequência do Sinal:<b>')

        # Slider para controlar a frequência do sinal de referência senoidal
        self.sl = slider(pos=self.scene.title_anchor, min=0.1, max=4,
                         value=1., length=220, right=15, bind=self.setfreq)
        
        # Caixa de texto para mostrar o valor real da frequência
        self.wt = wtext(pos=self.scene.title_anchor,
                        text='{:1.2f}'.format(self.sl.value))
        self.scene.append_to_title('')
        self.scene.append_to_title('\n\n<b>Amplitude do Sinal:<b>')

        # Slider para controlar a amplitude do sinal de referência senoidal
        self.sl2 = slider(pos=self.scene.title_anchor, min=0.1, max=1,
                    value=.1, length=220, right=15, bind=self.setAmp)
        # Caixa de texto para mostrar o valor real da frequência
        
        self.ampl = wtext(pos=self.scene.title_anchor,
                          text='{:1.2f}'.format(self.sl2.value))
        self.scene.append_to_title('\n\n')

        # Criando o menu de escolha do sinal de referência
        self.scene.append_to_title('<b>Sinal de Referência:</b>')
        self.scene.append_to_title(' ')


    def Menu(m):
        print('ok')

    # %% Criação do controlador interativo
    # Criando a função para escolher o tipo de controlador e fornecendo as matrizes


    def recebe_Ar(self, Ar):
        new_Ar = np.asarray(Ar)
        wtext(pos=self.scene.title_anchor,
              text='\n\n<b>Recebido</b>')
        print(new_Ar)
        type(new_Ar)


    def recebe_Br(self, Br):
        new_Ar = np.asarray(Br)
        wtext(pos=self.scene.title_anchor,
              text='\n\n<b>Recebido</b>')
        print(new_Ar)
        type(new_Ar)


    def recebe_K(self, K):
        new_Ar = np.asarray(K)
        wtext(pos=self.scene.title_anchor, text='\n\n<b>Recebido</b>')
        print(new_Ar)
        type(new_Ar)


    def check_action(self, x):
        if x.checked:
            self.text_1 = wtext(pos=self.scene.title_anchor,
                                text='<b>Tipo de Controlador:</b> ')
            self.MM = menu(pos=self.scene.title_anchor, choices=[
                    'Espaço de Estados', 'Função de Transferência'], bind=self.Menu)
            self.text_2 = wtext(pos=self.scene.title_anchor,
                        text='\n\n<b>Matriz Ar:</b> ')
            self.bt_1 = winput(pos=self.scene.title_anchor,
                        prompt='Enter here', type='string', bind=self.recebe_Ar)

            self.text_3 = wtext(pos=self.scene.title_anchor,
                        text='\n\n<b>Matriz Br:</b> ')
            self.bt_2 = winput(pos=self.scene.title_anchor,
                        prompt='Enter here', type='string', bind=self.recebe_Br)

            self.text_4 = wtext(pos=self.scene.title_anchor,
                        text='\n\n<b>Matriz K:</b> ')
            self.bt_3 = winput(pos=self.scene.title_anchor,
                        prompt='Enter here', type='string', bind=self.recebe_K)
            self.esp = wtext(pos=self.scene.title_anchor, text='\n\n')

        else:
            self.text_1.text = ""
            self.MM.delete()
            self.text_2.text = ""
            self.bt_1.delete()
            self.text_3.text = ""
            self.bt_2.delete()
            self.text_4.text = ""
            self.bt_3.delete()
            self.esp.text = ""

    def btn_controlador_interativo(self):
        # Criando o botão que chama o controlador interativo
        self.scene.append_to_title('\n\n')
        self.bt3 = checkbox(pos=self.scene.title_anchor,
                    text='<b>CONTROLE PERSONALIZADO</b>', bind=self.check_action)
        self.scene.append_to_title('\n\n')

