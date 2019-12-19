#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import serial.tools.list_ports
#import json
import matplotlib.pyplot as plt
#import matplotlib.collectmation as collectmation
from matplotlib.gridspec import GridSpec
#from mpl_toolkits.mplot3d import Axes3D
#import threading
import numpy as np
import datetime
import os 
import sys
from scipy.interpolate import splrep, splev
from termcolor import colored, cprint



TIEMPO_PRUEBA = 5 ##TIEMPO DE LA PRUEBA EN SEGUNDOS
DELAY = 1 ## DELAY DE LA PRUEBA EN MUESTRAS, PARA QUITAR ARTEFACTOS DE INICIO
SUAVIZADO = 10 ## SUAVIZADO DE LAS CURVAS
MARKER_SIZE = 5 ## TAMAÑO DE LA MARCA
BAR_SIZE = 0.4 ##ANCHO DE LAS BARRAS
##RAW
vx0 = [] #Tiempo
yaw0 = [] #YAW
pitch0 = [] #PITCH
roll0 = [] #ROLL
## SUAVIZADO
s_yaw0 = []
s_pitch0 = []
s_roll0 = []
## PUNTOS MAXIMOS
yaw0_max = []
pitch0_max = []
roll0_max = []
vx_yaw0 = []
vx_pitch0 = []
vx_roll0 = []
##HERTZ
hz_pitch0 = []
hz_roll0 = []
hz_yaw0 = []



##CONDICIONES
cond1 = False
cond2 = False
cond3 = False
cond4 = False
state_test = 1
state_loop = 1
###############
##ARCHIVOS
name_folder = "none"


##MAIN
def main():
    profilePatient()

    ok = True

    while (ok == True):
        loop()

##LOOP
def loop():
    global state_loop
    if (state_loop == 1):
        ardu()
        reset()
        selectTest()
        #smooth(SUAVIZADO)
        #buscar()
        #hertz_state()
        graph()
    if (state_loop == 2):
        logo()
        estado = input("Nueva Muestra? y/n: ")
        if (estado == 'y'):
            limpiar()
            reset()
            state_loop = 1
            main()

        else: 
            limpiar()
            print(Salir)
            exit()



##INGRESO DE DATOS DEL PACIENTE
def profilePatient():
    global name_folder, TIEMPO_PRUEBA
    logo()
    number_input =''
    try:
        TIEMPO_PRUEBA= int(input("Tiempo de Evaluación en Segundos [20] : ") or 20)
    except:
        print("solo puede escribir numeros, vuelva a intentarlo")
        time.sleep(1)
        profilePatient()

    while number_input == '':
        number_input=input("Id: ")
        if number_input == '':
            print("debe asignar un id")
            time.sleep(1)
            logo()

 

    name_input = input("Nombre: ")

    lastname_input = input("Apellido: ")
    age_input = input("Edad: ")
    height_input = float(input("Altura cm: "))
    weight_input = float(input("Peso kg: "))
    name_folder = number_input+"_"+name_input+"_"+lastname_input
    logo()
    print ("ID = ",colored(number_input, 'blue',attrs=['bold']))
    print ("TIEMPO MAXIMO PARA EL TUG = ",colored(TIEMPO_PRUEBA, 'blue',attrs=['bold']))
    print ("NOMBRE = ",colored(name_input, 'blue',attrs=['bold']),colored(lastname_input,'blue',attrs=['bold']))
    print ("EDAD = ", colored(age_input,'blue',attrs=['bold']))
    print ("ALTURA = ", colored(height_input,'blue',attrs=['bold']))
    print ("PESO = ",colored(weight_input,'blue',attrs=['bold']))
    IMC = round((weight_input)/((height_input/100)**2), 1)
    if IMC < 16:
        colorIMC = 'red'
        resIMC = 'Desnutrición severa'
    elif IMC >=16.1 and IMC <=18.4:
        colorIMC = 'magenta'
        resIMC = 'Desnutrición Moderada'
    elif IMC >=18.5 and IMC <=22:
        colorIMC = 'yellow'
        resIMC = 'Bajo Peso'
    elif IMC >=22.1 and IMC <=24.0:
        colorIMC = 'green'
        resIMC = 'Peso Normal'
    elif IMC >=25 and IMC <=29.9:
        colorIMC = 'yellow'
        resIMC = 'Sobrepeso'
    elif IMC >=30 and IMC <=34.9:
        colorIMC = 'magenta'
        resIMC = 'Obesidad tipo I'
    elif IMC >=35 and IMC <=39.9:
        colorIMC = 'red'
        resIMC = 'Obesidad tipo II'
    elif IMC >40:
        colorIMC = 'red'
        resIMC = 'Obesidad tipo II'

    print ("IMC = ",colored(IMC,colorIMC,attrs=['bold']), '-', colored(resIMC,colorIMC,attrs=['bold']))

    createPatient = input("¿Los datos son Correctos? y/n: ")

    if createPatient.lower() == "y":
        limpiar()
        createFolder()
        createLog(number_input, name_input, lastname_input, age_input, str(height_input), str(weight_input))

    else:
        main()

##CREA LA CARPETA
def createFolder():
    try:
        global name_folder
        os.makedirs(name_folder)
        logo()
        creado = colored(centerify('creado',80), 'green', attrs=['reverse'])
        print(creado)
    except OSError:
        print("Datos ya creados, favor utilice oto Id")
        main()

   
def selectTest():
    global state_test
    global vx0, yaw0, pitch0, roll0    
    global yaw0_max, pitch0_max, roll0_max, vx_yaw0, vx_pitch0, vx_roll0
    global hz_pitch0, hz_roll0, hz_yaw0
    state_test= input("Presione <enter> para comenzar:")
    if (cond1 == True):
        vx0 = []
        yaw0 = []
        pitch0 = []
        roll0 = []
        s_yaw0 = []
        s_pitch0 = []
        s_roll0 = []
        yaw0_max = []
        pitch0_max = []
        roll0_max = []
        vx_yaw0 = []
        vx_pitch0 = []
        vx_roll0 = []
        hz_pitch0 = []
        hz_roll0 = []
        hz_yaw0 = []
    collect()

##CREA LOG CON DATOS DEL PACIENTE
def createLog(number_input, name_input, lastname_input, age_input, height_input, weight_input):
	name_Log_profile = number_input+"\n"+name_input+"\n"+lastname_input+"\n"+age_input+"\n"+height_input+"\n"+weight_input
	Log_profile = name_folder+'/'+'profile.log'
	log = open(Log_profile, 'w')
	log.write(name_Log_profile)
	log.close()

##CONECCION DE ARDUINO
def ardu():
    #try:
    global arduino
    port = list(serial.tools.list_ports.comports())
    device = port[0]
    arduino = serial.Serial(device.device, 9600, timeout=1.)
    #time.sleep(2)
    #arduino.write(b'9')
    print("Receptor Conectado")
 #   except IndexError:
  #      raw_input("Conecte y presione <enter> tecla para volver a intentar")
   #     ardu()

##RESET DE ARDUINO
def reset():
    global arduino
    arduino.setDTR(False)
    time.sleep(1)
    arduino.flushInput()
    arduino.setDTR(True)


##RECOLECTA LOS DATOS
def collect():
    limpiar()
    global vx0, yaw0, pitch0, roll0, cond1
    Medir = colored(centerify('midiendo espere',80), 'red', attrs=['reverse'])
    print(Medir)
    cond1 = True
    date=datetime.datetime.now()
    log_test = open(name_folder+'/'+"C1"+"_"+str(date.day)+'-'+str(date.month)+'-'+str(date.year)+'_'+str(date.hour)+':'+str(date.minute)+str(date.second)+'.tug', 'a')
#    arduino.write(b'9')
    i = 0
    t = 0
    conteo = TIEMPO_PRUEBA
    try:
        while i <= TIEMPO_PRUEBA:
            data = []
            data.append(arduino.readline())
            data = [x.replace("\r\n","") for x in data]
            for line in data:
                Type = line.split(",")
                a = Type[0]
                b = Type[1]
                c = Type[2]
                d = Type[3]
                Line = (a+","+b+","+c+","+d+"\r\n")
                log_test.write(Line)
                #log_test.close()
                a = float(a)
                b = float(b)
                b = b * -1
                c = float(c)
                d = float(d)
    #           print("yaw:"+str(a)+" , "+"pitch:"+str(b)+","+"roll:"+str(c))
                if(len(vx0)==0):
                    t = t + d
                    d = d - t
                if(len(vx0)>=1):
                    d = d -t
                d = d/1000
                limpiar()
                print(Medir)
                print(d)
                i = d
                vx0.append(d)
                yaw0.append(c)
                pitch0.append(a)
                roll0.append(b)
    

    except ValueError:
        print ("Error en la comunicación, intente nuevamente...")
        print ("Intentanco recuperar comunicación")
        time.sleep(1)
        reset()
        collect()
    except IndexError:
        print ("Error de comunicación, revise bateria e intente nuevamente...")
        print ("Intentanco recuperar comunicación")
        time.sleep(1)
        reset()
        collect()


##CAMBIA EL ESTADO DEL BUSCADOR DE MAXIMOS
def buscar():
    global kz_vx
    hz_vx = 1
    buscar_maximos(s_yaw0[DELAY:], s_pitch0[DELAY:], s_roll0[DELAY:], vx0[DELAY:])

##BUSCA LOS MAXIMOS
def buscar_maximos(yaw, pitch, roll, vx):
    for pos in range(3):
        l = 0
        g = True
        if (pos==0):
            x_v = yaw
        if (pos==1):
            x_v = pitch
        if (pos==2):
            x_v = roll
        for i in range(len(x_v)):
            x = x_v[l]
            ix = i
            if (i == 0):
                ix = 0
            else:
                ix = i - 1
            if (x_v[ix] <= x):
                l=l+1
                g = True
            if (x_v[ix] > x):
                l=l+1
                if (g == True):
                    g = False
                    var = ix
                    global yaw0_max, pitch0_max, roll0_max, vx_yaw0, vx_pitch0, vx_roll0
                    if (pos == 0):
                        yaw0_max.append(x_v[var])
                        vx_yaw0.append(vx[var])
                    if (pos == 1):       
                        pitch0_max.append(x_v[var])
                        vx_pitch0.append(vx[var])
                    if (pos == 2):
                        roll0_max.append(x_v[var])
                        vx_roll0.append(vx[var])

##SUAVIZA LAS CURVAS
def smooth(smooth):
        global s_yaw0, s_pitch0, s_roll0
        b_yaw0 = splrep(vx0,yaw0,s=smooth)
        s_yaw0 = splev(vx0,b_yaw0)
        b_pitch0 = splrep(vx0,pitch0,s=smooth)
        s_pitch0 = splev(vx0,b_pitch0)
        b_roll0 = splrep(vx0,roll0,s=smooth)
        s_roll0 = splev(vx0,b_roll0)



def hertz_state():
    global kz_vx
    hertz(vx_yaw0, vx_pitch0, vx_roll0)


def hertz(vx_yaw, vx_pitch, vx_roll):
    global hz_yaw0, hz_pitch0, hz_roll0

    for pos in range(3):
        if (pos==0):
            mark = vx_yaw
        if (pos==1):
            mark = vx_pitch
        if (pos==2):
            mark = vx_roll
        n = len(mark)
        s_pos0 = 0
        s_pos1 = 0 
        for i in range(TIEMPO_PRUEBA):
            l =[]
            s_pos1 = s_pos1+1
            for i in mark:
                if i < s_pos1 and i > s_pos0:
                    l.append(1)
                if i > s_pos1:
                    break
            s_pos0 = s_pos1 - 1
            if (pos == 0):
                hz_yaw0.append(len(l))
            if (pos == 1):       
                hz_pitch0.append(len(l))
            if (pos == 2):
                hz_roll0.append(len(l))

##GRAFICAMOS
def graph():
    global state_loop
    
    plt.switch_backend('TkAgg') #default on my system
    print(('Backend: {}'.format(plt.get_backend())))

    f = plt.figure(num="TUG", figsize=(20,15))
    mng = plt._pylab_helpers.Gcf.figs.get(f.number, None)

    #mng.window.showMaximized()


    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.title("TUG con acelerometria")

    gs1 = GridSpec(5, 8)
    gs1.update(left=0.05, right=0.95, wspace=0.5, hspace=0.3, bottom=0.08)



    ax2 = plt.subplot(gs1[1, :])
    ax2.grid()
    ax2.set_ylabel('Pitch',fontsize=8)
    L1 = ax2.plot(vx0[DELAY:],pitch0[DELAY:])
    #ax2.plot(vx_pitch0, pitch0_max, 'gv', markersize=MARKER_SIZE)

     
    ax3 = plt.subplot(gs1[2, :])
    ax3.grid()
    ax3.set_ylabel('Roll',fontsize=8)
    L1 = ax3.plot(vx0[DELAY:],roll0[DELAY:])
    #ax3.plot(vx_roll0, roll0_max, 'gv', markersize=MARKER_SIZE)


    ax4 = plt.subplot(gs1[3, :]) 
    ax4.grid()
    ax4.set_ylabel('Yaw',fontsize=8)
    L1 = ax4.plot(vx0[DELAY:],yaw0[DELAY:])
    #ax4.plot(vx_yaw0, yaw0_max, 'gv', markersize=MARKER_SIZE)

    #xl = np.arange(len(hz_pitch0))

    date=datetime.datetime.now()
    name = (name_folder+'/'+"IMG"+"_"+str(date.day)+'-'+str(date.month)+'-'+str(date.year)+'_'+str(date.hour)+':'+str(date.minute)+':'+str(date.second)+'.png')
    plt.savefig(name, bbox_inches='tight')
    state_loop = 2
    plt.show()
    limpiar()


def centerify(text, width=-1):
  lines = text.split('\n')
  width = max(list(map(len, lines))) if width == -1 else width
  return '\n'.join(line.center(width) for line in lines)


def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')


def logo():
    limpiar()
    print(banner)
    print("\n\n")






#####Textos de Aviso
banner = colored(centerify('Full Axis V0.5 - Tesis TUG',80), 'white', attrs=['reverse'])
Salir = colored(centerify('Hasta la vista',80), 'green', attrs=['reverse'])



if __name__ == "__main__":
    main()








