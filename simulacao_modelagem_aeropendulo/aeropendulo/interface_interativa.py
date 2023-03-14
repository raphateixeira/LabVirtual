import vpython as vp


class Interface:
    # ############# INICIO SESSÃO - TESTE MUNU INTERATIVO ##############
    def __init__(self, animacao_aeropendulo) -> None:
        self.EXE = False
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

    def criar_interface(self) -> None:
        self.scene.append_to_caption(
            "\tMenu Interativo Aeropêndulo\n")
        self.scene.append_to_caption("\tRefazer Simulação\n\n")
        self.scene.append_to_caption("\t ")
        self.buttom_exe = vp.button(bind=self.executar,
                                    text="Excecutar",
                                    color=vp.color.white,
                                    background=vp.color.red)
        self.scene.append_to_caption("\n\n")
