# ----------------------------------------------------
# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# ----------------------------------------------------
#
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Tema: Simulação MAGLEV
# Autor: Yuri de Oliveira Cota
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
#  ----------------------------------------------------
#

import vpython as vp


class AniMAGLEV:
    """Classe que implementa a animação do MAGLEV"""

    def __init__(self, a):

        # Set de funções
        self.constrain = False
        self.grid = None
        self.drag = False

        # Parâmetros da cena da animação
        self.scene = vp.canvas(title="<b>SIMULAÇÃO MAGLEV V1.0<b>\n\n",
                               width=700,
                               height=445,
                               align="left",
                               background=vp.color.white,
                               foreground=vp.color.black,
                               userspin=False)

        # Chamando a função para criar a animação gráfica do MAGLEV
        self.maglev = self.animation()

        def animation(self):
            # Ambiente da simulação

            # Mesa
            self.mesa = vp.box(pos=vp.vec(5e-2, -9e-2, 0),
                               size=vp.vec(20e-2, 1e-2, 10e-2),
                               color=vp.vec(0.570, 0.259, 0.103))

            # Estrutura de suporte da Bobina

            # Suporte 1
            self.suporte_1 = vp.cylinder(pos=vp.vec(14e-2, -8.5e-2, 0),
                                         size=vp.vec(17e-2, 0.8e-2, 0.8e-2),
                                         color=vp.vec(0.618, 0.668, 0.636),
                                         axis=vp.vec(0, 1, 0))

            # Conexão 1
            self.conexao_1 = vp.sphere(pos=vp.vec(14e-2, 8e-2, 0),
                                       radius=1e-2,
                                       color=vp.vec(0.618, 0.668, 0.636))

            # Suporte 2
            self.suporte_2 = vp.cylinder(pos=vp.vec(0, 8e-2, 0),
                                         size=vp.vec(14e-2, 0.8e-2, 0.8e-2),
                                         color=vp.vec(0.618, 0.668, 0.636),
                                         axis=vp.vec(0, 0, 0))

            # Conexão 2
            self.conexao_2 = vp.sphere(pos=vp.vec(0, 8e-2, 0),
                                       radius=1e-2,
                                       color=vp.vec(0.618, 0.668, 0.636))

            # Suporte 3
            self.suporte_3 = vp.cylinder(pos=vp.vec(0, 5e-2, 0),
                                         size=vp.vec(3e-2, 0.8e-2, 0.8e-2),
                                         color=vp.vec(0.618, 0.668, 0.636),
                                         axis=vp.vec(0, 1, 0))

            # Suporte completo
            self.sup_comp = vp.compound(
                [self.suporte_1, self.conexao_1, self.suporte_2, self.conexao_2, self.suporte_3])

            # Mesa + Suporte
            self.mesa_sup = vp.compound([self.mesa, self.sup_comp])

            # Eletroimã

            # Bobina 1
            self.bobina_1 = vp.cylinder(pos=vp.vec(0, 4.5e-2, 0),
                                        size=vp.vec(0.5e-2, 6e-2, 6e-2),
                                        color=vp.vec(0.0, 0.568, 0.864),
                                        axis=vp.vec(0, 1, 0))

            # Bobina 2
            self.bobina_2 = vp.cylinder(pos=vp.vec(0, 0.5e-2, 0),
                                        size=vp.vec(4e-2, 4e-2, 4e-2),
                                        color=vp.vec(1.0, 0.387, 0.0),
                                        axis=vp.vec(0, 1, 0))

            # Bobina 3
            self.bobina_3 = vp.cylinder(pos=vp.vec(0, 0, 0),
                                        size=vp.vec(0.5e-2, 6e-2, 6e-2),
                                        color=vp.vec(0.0, 0.568, 0.864),
                                        axis=vp.vec(0, 1, 0))

            # Eletroimão completo
            self.eletro = vp.compound(
                [self.bobina_1, self.bobina_2, self.bobina_3])

            # Parâmetros do cilindro flutuante
            self.L_cilindro = 5e-2
            self.r_cilindro = 1e-2
            self.cil = vp.cylinder(pos=vp.vec(12e-2, -3.5e-2, 0),
                                   axis=vp.vec(0, -self.L_cilindro, 0),
                                   color=vp.vec(0.902, 0.827, 0),
                                   radius=self.r_cilindro,
                                   velocity=vp.vector(0, 0, 0))
        return self.cil
