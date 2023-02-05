import vpython as vp


def graficos():
    titulo = "Gráficos dos estados do Pêndulo Simples"
    grafico = vp.graph(title=titulo, align="right", xtitle='tempo (s)',
                       fast=True, width=650, height=550,
                       center=vp.vector(0, 12, 0), scroll=True,
                       xmin=0, xmax=5, ymin=-35, ymax=35, dot=True,
                       background=vp.vector(0.95, 0.95, 0.95))

    curva1 = vp.gcurve(color=vp.color.blue, width=3,
                       markers=False, label="Posição Angular do Pêndulo",
                       dot=True, dot_color=vp.color.blue)

    curva2 = vp.gcurve(color=vp.color.red, width=3,
                       markers=False, label="Velocidade Angular do Pêndulo",
                       dot=True, dot_color=vp.color.red)

    curva3 = vp.gcurve(color=vp.color.orange, width=3,
                       markers=False, label="Aceleração Angular do Pêndulo",
                       dot=True, dot_color=vp.color.orange)
    return grafico, curva1, curva2, curva3
