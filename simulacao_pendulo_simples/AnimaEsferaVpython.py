from vpython import *

running = True

def Run(b):
    global running, remember_dt, dt
    running = not running
    if running:
        b.text = 'Pause'
        remember_dt = dt
        dt = 0
    else:
        b.text = 'Run'
        remember_dt = dt
        dt = 0
    return

button(text='Pause', pos = scene.title_anchor, bind=Run)


posicao_esfera = vec(2,2,2)
esfera = sphere(radius = 0.2,
                make_trail = True,
                color = color.red )
dt = 0.1
t = 0
while True:
    rate(10)
    esfera.pos = vector(cos(t),sin(t),cos(t/2))
    t += dt
