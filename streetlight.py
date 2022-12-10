from tkinter import *
import time


WIDTH=1920
HEIGHT=1080
ptom=50

window=Tk()

canvas=Canvas(window,width=WIDTH,height=HEIGHT)
canvas.pack()

#считывает машины, сначала координату, потом скорость
# pos speed

carsx1=[]
carsy1=[]
carblue=PhotoImage(file='bruh1.png')
carred=PhotoImage(file='car1.png')

with open('carsx1.txt','r') as file:
    for i in file.readlines():
        a=list(map(int,i.split()))
        a.append(canvas.create_image(-a[0]*ptom,400,image=carblue,anchor=NW))
        carsx1.append(a)
        

with open('carsy1.txt','r') as file:
    for i in file.readlines():
        a=list(map(int,i.split()))
        a.append(canvas.create_image(900,500-a[0]*ptom,image=carred))
        carsy1.append(a)
        


#переменные, мин промежуток времени, макс скорость, ускорение/замедление
dt=1/24
max_speed=50/3
dv=max_speed/7
cycle=60


#как ведут себя машины на жёлтом/красном
def stop(cars,dir):
    for i in range(len(cars)):
            #едет вперед со своей скоростью
            if dir:
                canvas.move(cars[i][-1],cars[i][1]*ptom*dt,0)
            else:
                canvas.move(cars[i][-1],0,cars[i][1]*ptom*dt)
            cars[i][0]-=cars[i][1]*dt

            #смотрит расстояние до светофора/ближайшей машины спереди
            if i:
                #если близко и едет, то замедляемя
                if 0<cars[i][0]-cars[i-1][0]<60 and cars[i][1]>0 and cars[i-1][1]<max_speed:
                  cars[i][1]-=dt*dv
                  if cars[i][1]<0:
                    cars[i][1]=0
            
                #иначе если не на макс скорости, то ускоряемся
                elif 0<cars[i][1]<max_speed:
                    cars[i][1]+=dt*dv
                    if cars[i][1]>max_speed:
                        cars[i][1]=max_speed
            else:
                #если близко и едет, то замедляемя
                if 0<cars[i][0]<60 and cars[i][1]>0:
                  cars[i][1]-=dt*dv
                  if cars[i][1]<0:
                    cars[i][1]=0
            
                #иначе если не на макс скорости, то ускоряемся
                elif 0<cars[i][1]<max_speed:
                    cars[i][1]+=dt*dv
                    if cars[i][1]>max_speed:
                        cars[i][1]=max_speed


#как машины ведут себя на зеленом
def go(cars,dir):
    for car in cars:
            if dir:
                canvas.move(car[-1],car[1]*ptom*dt,0)
            else:
                canvas.move(car[-1],0,car[1]*ptom*dt)
            car[0]-=car[1]*dt
            if car[1]<max_speed:
                car[1]+=dt*dv
                if car[1]>max_speed:
                    car[1]=max_speed


for cyc in range(10):

    incoming_x=0
    incoming_y=0
    
    #смотрим сколько машин в 100м от светофора в каждом направлении
    for car in carsx1:
        if car[0]<100:
            incoming_x+=1

    for car in carsy1:
        if car[0]<100:
            incoming_y+=1

    print(incoming_x,incoming_y)
    #распределяем время соответсвено
    if incoming_x==incoming_y:
        green=int(cycle/(2*dt))
    else:
        weight=incoming_x/(incoming_x+incoming_y)
        print(cycle,weight,dt,cycle*weight/dt)
        green=int(cycle*weight/dt)

    #говорит что должны делать машины на зеленый,желтый,красный,желтый соответсвено
    print('green',green)
    for i in range(green):
        go(carsx1,1)
        stop(carsy1,0)
        window.update()
        time.sleep(dt)
    print('yellow')
    for i in range(int(7/dt)):
        stop(carsx1,1)
        stop(carsy1,0)
        window.update()
        time.sleep(dt)
    print('red',int(cycle/dt)-green)
    for i in range(int(cycle/dt)-green):
        stop(carsx1,1)
        go(carsy1,0)
        window.update()
        time.sleep(dt)
    print('yellow')
    for i in range(int(7/dt)):
        stop(carsx1,1)
        stop(carsy1,0)
        window.update()
        time.sleep(dt)
        
