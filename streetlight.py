from tkinter import *
import time
from math import exp

#переменные, мин промежуток времени, макс скорость, ускорение/замедление
dt=1/24
max_speed=50/3
dv=max_speed/7

render=((input("Показывать движение машин? Y/N ")).lower())=='y'

smart=((input("Использовать умный светофор? Y/N ")).lower())=='y'

x=int(input("Введите количество машин с запада: "))
y=int(input("Введите количество машин с севера: "))

if render:
    WIDTH=599
    HEIGHT=600
    ptom=50

    window=Tk()

    canvas=Canvas(window,width=WIDTH,height=HEIGHT)
    canvas.pack()
    
    bg_img=PhotoImage(file="bg.png")
    bg=canvas.create_image(0,0,image=bg_img,anchor=NW)

    red_img=PhotoImage(file='red.png')
    yellow_img=PhotoImage(file='yellow.png')
    green_img=PhotoImage(file='green.png')
    redlight=canvas.create_image(1400,1380,image=red_img,anchor=NW)
    yellowlight=canvas.create_image(1400,1380,image=yellow_img,anchor=NW)
    greenlight=canvas.create_image(400,380,image=green_img,anchor=NW)


if render:
    carblue=PhotoImage(file='car0.png')
    carred=PhotoImage(file='car1.png')
    carsx1=[[1000,max_speed,canvas.create_image(-3000*ptom,300,image=carblue,anchor=NW)]]
    for i in range(x):
        carsx1.append([3*i,max_speed,canvas.create_image(100-3*i*ptom,300,image=carblue,anchor=NW)])
    carsy1=[[1000,max_speed,canvas.create_image(-3000*ptom,300,image=carred,anchor=NW)]]
    for i in range(y):
        carsy1.append([10+3*i,0,canvas.create_image(330,100-3*i*ptom,image=carred,anchor=N)])



else:
    carsx1=[[1000,max_speed]]
    for i in range(x):
        carsx1.append([3*i,max_speed])
    carsy1=[[1000,max_speed]]
    for i in range(y):
        carsy1.append([10+3*i,0])



window.mainloop()


#как ведут себя машины на жёлтом/красном
def stop(cars,dir):
    for i in range(len(cars)):
            #едет вперед со своей скоростью
            if render:
                if dir:
                    canvas.move(cars[i][-1],cars[i][1]*ptom*dt,0)
                else:
                    canvas.move(cars[i][-1],0,cars[i][1]*ptom*dt)
            cars[i][0]-=cars[i][1]*dt

            #смотрит расстояние до светофора/ближайшей машины спереди
            if i!=0 and cars[i-1][0]>0:
                #если близко и едет, то замедляемя
              #  print('Номер,позиция,скорость для тек и пред',i,cars[i][0],cars[i][1],cars[i-1][0],cars[i-1][1])
                if (0<=(cars[i][0]-cars[i-1][0])<60) and cars[i][1]>0 and cars[i-1][1]<max_speed :
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
            if render:
                if dir:
                    canvas.move(car[-1],car[1]*ptom*dt,0)
                else:
                    canvas.move(car[-1],0,car[1]*ptom*dt)
            car[0]-=car[1]*dt
            if car[1]<max_speed:
                car[1]+=dt*dv
                if car[1]>max_speed:
                    car[1]=max_speed

going_x=True
going_y=True

time_elapsed=0

while going_x or going_y:

        incoming_x=0
        incoming_y=0
        
        #смотрим сколько машин в 100м от светофора в каждом направлении
        for car in carsx1:
            if 0<car[0]<100:
                incoming_x+=1

        for car in carsy1:
            if 0<car[0]<100:
                incoming_y+=1

        #распределяем время соответсвено
        if smart:
            green=int(10*incoming_x/dt)
            
            red=int(10*incoming_y/dt)

        else:
            green,red=int(30/dt),int(30/dt)

        #говорит что должны делать машины на зеленый,желтый,красный,желтый соответсвено
        for i in range(green):
            go(carsx1,1)
            stop(carsy1,0)
            if render:
                window.update()
                time.sleep(dt)
            time_elapsed+=dt
            if carsx1[-1][0]<0:
                going_x=False
            if carsy1[-1][0]<0:
                going_y=False
            if not (going_x or going_y):
                break

        if render:
            canvas.move(greenlight,1000,1000)
            canvas.move(yellowlight,-1000,-1000)

        for i in range(int(7/dt)):
            stop(carsx1,1)
            stop(carsy1,0)
            if render:
                window.update()
                time.sleep(dt)
            time_elapsed+=dt
            if carsx1[-1][0]<0:
                going_x=False
            if carsy1[-1][0]<0:
                going_y=False
            if not (going_x or going_y):
                break

        if render:
            canvas.move(yellowlight,1000,1000)
            canvas.move(redlight,-1000,-1000)

        for i in range(red):
            stop(carsx1,1)
            go(carsy1,0)
            if render:
                window.update()
                time.sleep(dt)
            time_elapsed+=dt
            if carsx1[-1][0]<0:
                going_x=False
            if carsy1[-1][0]<0:
                going_y=False
            if not (going_x or going_y):
                break

        if render:
            canvas.move(redlight,1000,1000)
            canvas.move(yellowlight,-1000,-1000)

        for i in range(int(7/dt)):
            stop(carsx1,1)
            stop(carsy1,0)
            if render:
                window.update()
                time.sleep(dt)
            time_elapsed+=dt
            if carsx1[-1][0]<0:
                going_x=False
            if carsy1[-1][0]<0:
                going_y=False
            if not (going_x or going_y):
                break
        if not (going_x or going_y):
            break

        if render:
            canvas.move(redlight,1000,1000)
            canvas.move(greenlight,-1000,-1000)

print("Время чтобы все машины проехали перекрёсток: ", time_elapsed)