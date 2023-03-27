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
from .graficos_aeropendulo import Graficos                  # noqa: F401
from .animacao_aeropendulo import AnimacaoAeropendulo       # noqa: F401
from .interface_interativa import Interface                 # noqa: F401
from .modelo_mat_aeropendulo import ModeloMatAeropendulo    # noqa: F401
from .implementacao_controlador import ControladorDiscreto  # noqa: F401


__version__ = "0.1.0"
