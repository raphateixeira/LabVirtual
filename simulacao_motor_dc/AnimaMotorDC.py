from vpython import *
import numpy as np

g = 'Grafico'
grafico = graph(title = g, xtitle = 'tempo (s)',ytitle = 'amplitude' ,fast = True, width = 800)
curva = gcurve(color=color.blue , width = 4 , markers=False, label='Curva')


base=pyramid(pos=vector(0,-3,0),  axis=vector(0,1,0),size=vector(2,4,2),color=color.white)
corpo1 = cylinder(pos=vector(-2.5,0,0),radius=5,color=color.gray(0.5) ,size=vector(5,5,5),texture='https://media.istockphoto.com/id/949442622/pt/foto/shiny-metallized-foil-texture-surface-for-background.jpg?s=612x612&w=is&k=20&c=-k6ud-30xVPQNMSK4g-2Fxy3HwZ9ycqz27dMNgVljZg=')
corpo2 = cylinder(pos=vector(-2,0,0),radius=2.5,color=color.gray(0.65),size=vector(5,2,2))
eixo = cylinder(pos=vector(0,0,0),radius=0.5,color=color.gray(0.9),size=vector(8,1,1),texture='https://static.vecteezy.com/ti/vetor-gratis/t2/1857360-metal-textura-fundo-vetor.jpg')

#ref1 = arrow(pos=vector(7.9,0.3,0), color=color.magenta  ,   axis=vector(0,1,0), shaftwidth=0.1)
#ref2 = arrow(pos=vector(7.9,0,-0.3),     color=color.magenta, axis=vector(0,0,-1), shaftwidth=0.1)
#ref3 = arrow(pos=vector(7.9,0,0.3),    color=color.magenta,  axis=vector(0,0,1), shaftwidth=0.1)
#ref4 = arrow(pos=vector(7.9,-0.3,0),  color=color.magenta,    axis=vector(0,-1,0), shaftwidth=0.1)

ng = 0.9
nm = 0.69
Kg = 70
Kt = 0.00767
Km = Kt
Jm = 3.87*10**(-7)
Jeq = 2*10**(-3)
Rm = 2.6
Beq =4*10**(-3)
Ts = 0.1
m = 0.2
b = 0.2
k = 1.2

def MDC(x):
    x1, x2 = x
    dx1 = x2
    dx2 = -(0)*x1 - ((Beq*Rm + ng*nm*Km*Kt*Kg**2 * Jm)/(Jeq*Rm))*x2 + (1/Jeq*Rm)*0

    dx = np.array([dx1, dx2])

    xn = x + Ts*dx
    return xn


t = 0.0
x = np.array([0, 65])

while (t<15.0):
    sleep(Ts)
    print(x)
    x = MDC(x) 
    t = t + Ts
    omega = 2*pi/5*x[0] #vec(1,0,0)
    eixo.rotate(angle=omega*Ts,axis=vector(1,0,0))
    curva.plot(t,x[0])