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


class Interface:
    # ############# INICIO SESSÃO - TESTE MUNU INTERATIVO ##############
    def __init__(self, animacao_aeropendulo, controlador) -> None:
        self.EXE = False
        # controlador
        self.controlador = controlador

        self.animacao_aeropendulo = animacao_aeropendulo
        self.scene = animacao_aeropendulo.scene

        # Criando a interface
        self.criar_interface()

    def executar(self, b) -> None:
        if self.EXE:
            b.text = "Executar"
        else:
            b.text = "Pausar"
        self.EXE = not self.EXE

    def slide_angle_up(self, angle) -> None:
        self.animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                     angle=angle.value*0.01,
                                                     origin=vp.vec(0, 5.2, 0))

    def slide_angle_down(self, angle) -> None:
        self.animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                     angle=angle.value*0.01,
                                                     origin=vp.vec(0, 5.2, 0))
        # print("teste", angle.value)

    def slide_angle_referencia(self, valor):
        self.controlador.r = valor.value
        print(valor.value)

    def criar_interface(self) -> None:
        self.scene.append_to_caption(
            "\tMenu Interativo Aeropêndulo\n")
        self.scene.append_to_caption("\tRefazer Simulação\n\n")
        self.scene.append_to_caption("\t ")
        self.buttom_exe = vp.button(bind=self.executar,
                                    text="Excecutar",
                                    color=vp.color.white,
                                    background=vp.color.red)
        self.scene.append_to_caption("\n\n\t")
        self.scene.append_to_caption("Ângulo +  :  ")
        vp.slider(bind=self.slide_angle_up, min=0, max=5,
                  step=0.001, value=0)
        self.scene.append_to_caption("\n\n\t")
        self.scene.append_to_caption("Ângulo -   :  ")
        vp.slider(bind=self.slide_angle_down, min=-5, max=0,
                  step=0.001, value=-5)
        self.scene.append_to_caption("\n\n\t")
        self.scene.append_to_caption("Referência : ")
        vp.slider(bind=self.slide_angle_referencia, min=0, max=3,
                  step=0.001, value=0)
        self.scene.append_to_caption("\n\n")
