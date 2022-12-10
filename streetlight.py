from tkinter import *
import time

'''
на потом

WIDTH=500
HEIGHT=500

window=Tk()

canvas=Canvas(window,width=WIDTH,height=HEIGHT)
#canvas.pack()
'''


#while True:

# pos speed

carsx1=[]
carsy1=[]
with open('carsx1.txt','r') as file:
    for i in file.readlines():
        carsx1.append(list(map(int,i.split())))
with open('carsy1.txt','r') as file:
    for i in file.readline():
        carsy1.append(list(map(int,i.split())))

dt=1/1000
max_speed=50/3
dv=max_speed/7

def stop(cars):
    for i in range(len(cars)):
            cars[i][0]-=cars[i][1]*dt
            if i:
                a=min(cars[i][0]-cars[i-1][0],cars[i][0])
            else:
                a=cars[0][0]
            if 0<a<60 and cars[i][1]>0:
                cars[i][1]-=dt*dv
            elif cars[i][0]<max_speed:
                cars[i][1]+=dt*dv


def go(cars):
    for car in cars:
            car[0]-=car[1]*dt
            if car[1]<max_speed:
                car[1]+=dt*dv

for cycle in range(10):
    incoming_x=0
    incoming_y=0
    for car in carsx1:
        if car[0]<100:
            incoming_x+=1

    for car in carsy1:
        if car[0]<100:
            incoming_y+=1
    if incoming_x==incoming_y:
        green=60/dt
    else:
        weight=incoming_x/(incoming_x+incoming_y)
        green=int(120*incoming_x/(dt*weight))
    for i in range(green):
        go(carsx1)
        stop(carsy1)
    for i in range(7/dt):
        stop(carsx1)
        stop(carsy1)
    for i in range(120/dt-green):
        stop(carsx1)
        go(carsy1)
    for i in range(7/dt):
        stop(carsx1):
        stop(carsy1)
