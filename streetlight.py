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


#считывает машины, сначала координату, потом скорость
# pos speed


carsx1=[]
carsy1=[]
with open('carsx1.txt','r') as file:
    for i in file.readlines():
        carsx1.append(list(map(int,i.split())))
with open('carsy1.txt','r') as file:
    for i in file.readline():
        carsy1.append(list(map(int,i.split())))

#переменные, мин промежуток времени, макс скорость, ускорение/замедление
dt=1/1000
max_speed=50/3
dv=max_speed/7


#как ведут себя машины на жёлтом/красном
def stop(cars):
    for i in range(len(cars)):
            #едет вперед со своей скоростью
            cars[i][0]-=cars[i][1]*dt

            #смотрит расстояние до светофора/ближайшей машины спереди
            if i:
                a=min(cars[i][0]-cars[i-1][0],cars[i][0])
            
            else:
                a=cars[0][0]
            
            #если близко и едет, то замедляемя
            if 0<a<60 and cars[i][1]>0:
                cars[i][1]-=dt*dv
            
            #иначе если не на макс скорости, то ускоряемся
            elif cars[i][0]<max_speed:
                cars[i][1]+=dt*dv

#как машины ведут себя на зеленом
def go(cars):
    for car in cars:
            car[0]-=car[1]*dt
            if car[1]<max_speed:
                car[1]+=dt*dv


for cycle in range(10):

    incoming_x=0
    incoming_y=0
    
    #смотрим сколько машин в 100м от светофора в каждом направлении
    for car in carsx1:
        if car[0]<100:
            incoming_x+=1

    for car in carsy1:
        if car[0]<100:
            incoming_y+=1

    #распределяем время соответсвено
    if incoming_x==incoming_y:
        green=60/dt
    else:
        weight=incoming_x/(incoming_x+incoming_y)
        green=int(120*incoming_x/(dt*weight))

    #говорит что должны делать машины на зеленый,желтый,красный,желтый соответсвено
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
        stop(carsx1)
        stop(carsy1)
