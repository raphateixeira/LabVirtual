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
    """
    Classe que implementa a interface interativa do simulador do Aeropêndulo.

    Atributo:
        animacao_aeropendulo: Instância da classe AnimacaoAeropendulo.
        controlador: Instância da classe AnimacaoAeropendulo.
    """
    def __init__(self, animacao_aeropendulo, controlador) -> None:
        self.EXE = False
        self.valor_angle = 0.0
        self.controlador = controlador
        self.animacao_aeropendulo = animacao_aeropendulo
        self.scene = animacao_aeropendulo.scene

        # Criando a interface
        self.__criar_interface()

    def __executar(self, b) -> None:
        if self.EXE:
            self.animacao_aeropendulo.girar_helice()
            b.text = "Executar"
        else:
            b.text = "Pausar"
            self.animacao_aeropendulo.pause_giro()
        self.EXE = not self.EXE

    def rotate(self, angle) -> None:
        self.valor_angle = (angle.number)*(vp.pi/180.0)
        self.animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                     angle=self.valor_angle,
                                                     origin=vp.vec(0, 5.2, 0))
        self.animacao_aeropendulo.set_posicao_helice(self.valor_angle)

    def __slide_angle_referencia(self, valor) -> None:
        self.controlador.r = valor.value
        print(valor.value)

    def __criar_interface(self) -> None:
        self.scene.append_to_caption(
            "\tMenu Interativo Aeropêndulo\n")
        self.scene.append_to_caption("\n\t ")
        self.buttom_exe = vp.button(bind=self.__executar,
                                    text="Excecutar",
                                    color=vp.color.white,
                                    background=vp.color.red,
                                    width=100, _height=40)
        self.scene.append_to_caption("\t\t")
        self.scene.append_to_caption(
            "Posição Inicial\t")
        vp.winput(bind=self.rotate, prompt="Rotate: ", type="numeric",
                  width=100, _height=40)
        vp.wtext(text=" Graus")
        self.scene.append_to_caption('\n')

        self.scene.append_to_caption("\n\n\t")
        self.scene.append_to_caption("Referência : ")
        vp.slider(bind=self.__slide_angle_referencia, min=0, max=2,
                  step=0.001, value=0)
        self.scene.append_to_caption("\n\n")
