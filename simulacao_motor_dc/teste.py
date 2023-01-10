from vpython import *
import time
import numpy as np

def readFloat(fname, last):
		try:
			file = open(fname, 'r')
			val = float(file.read())
			file.close()
			return val
		except:
			return last



def writeFloat(fname, val):
	file = open(fname, 'w')
	file.write("{:.3f}".format(val))
	file.close()

axisArrowX = arrow(pos = vector(0,0,0), axis = vector(15,0,0), shaftwidth = .1, color = vector(1,0,0))
axisArrowY = arrow(pos = vector(0,0,0), axis = vector(0,15,0), shaftwidth = .1, color = vector(0,1,0))
axisArrowZ = arrow(pos = vector(0,0,0), axis = vector(0,0,15), shaftwidth = .1, color = vector(0,0,1))

#obj = box(pos = vector(0,10,0), size = vector(10,1,10))
wheel      = cylinder(pos=vector(0,0,  1.5), axis=vector(  0,  0,  2), radius=4, texture={'file':textures.rug , 'place':'right'} )
wheelArrow = arrow(   pos=vector(0,0,  1.5), axis=vector( 10,  0,  0), shaftwidth = .3, color = vector(0,1,1))
motor      = box(     pos=vector(0,0, -1.5), size=vector(  9,  9,  4), texture={'file':textures.gravel, 'place':'right'} )
motorArrow = arrow(   pos=vector(0,0, -1.5), axis=vector( 10,  0,  0), shaftwidth = .3, color = vector(0,1,1))

wheel_momentumInertia = 10
motor_momentumInertia = 30



wheel_angularVelocity = 1
motor_angularVelocity = 0

relative_angularSpeed = wheel_angularVelocity - motor_angularVelocity

wheel_angularAcceleration = 0
motor_angularAcceleration = 0


torque = 60
dt = 0.001
alpha = 10
while True:
	torque = readFloat("torque.txt", torque)
	torque_ = torque - alpha* relative_angularSpeed
	

	wheel_angularAcceleration =  torque_ / wheel_momentumInertia 
	motor_angularAcceleration = -torque_ / motor_momentumInertia
	
	wheel_angularVelocity += wheel_angularAcceleration * dt
	motor_angularVelocity += motor_angularAcceleration * dt

	relative_angularSpeed = wheel_angularVelocity - motor_angularVelocity

	print(torque, torque_, wheel_angularVelocity, motor_angularVelocity, relative_angularSpeed, motorArrow.axis )

	wheel.rotate(angle = wheel_angularVelocity*np.pi/180, axis=vec(0,0,1), origin=vector(0,0,1000))
	motor.rotate(angle = motor_angularVelocity*np.pi/180, axis=vec(0,0,1), origin=vector(0,0,1000))
	wheelArrow.rotate(angle = wheel_angularVelocity*np.pi/180, axis=vec(0,0,1), origin=vector(0,0,1000))
	motorArrow.rotate(angle = motor_angularVelocity*np.pi/180, axis=vec(0,0,1), origin=vector(0,0,1000))

	writeFloat("motor.txt", np.arctan2(motorArrow.axis.x, motorArrow.axis.y)*180/np.pi)
	time.sleep(dt)