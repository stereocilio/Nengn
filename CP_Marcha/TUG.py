#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import serial.tools.list_ports
#import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
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
        borrarDatos()
    if (state_loop == 2):
        logo()
        estado = input("Nuevo usuario? y/n: ")
        if (estado == 'y'):
            limpiar()
            reset()
            state_loop = 1
            main()

        else: 
            limpiar()
            print(Salir)
            exit()
    if(state_loop == 3):
            ardu()
            reset()
            selectTest()
            graph()
            borrarDatos()


##INGRESO DE DATOS DEL PACIENTE
    global name_folder, TIEMPO_PRUEBA
    logo()
    number_input =''
    try:
        TIEMPO_PRUEBA= int(eval(input("Tiempo de Evaluación en Segundos [20] : ")) or 20)
    except:
        print("solo puede escribir numeros, vuelva a intentarlo")
        time.sleep(1)
        profilePatient()

    while number_input == '':
        number_input=eval(input("Id: "))
        if number_input == '':
            print("debe asignar un id")
            time.sleep(1)
            logo()


    name_input = eval(input("Nombre: "))

    lastname_input = eval(input("Apellido: "))
    age_input = eval(input("Edad: "))
    height_input = float(eval(input("Altura cm: ")))
    weight_input = float(eval(input("Peso kg: ")))
    name_folder = number_input+"_"+name_input+"_"+lastname_input
    logo()
    print(("ID = ",colored(number_input, 'blue',attrs=['bold'])))
    print(("TIEMPO MAXIMO PARA EL TUG = ",colored(TIEMPO_PRUEBA, 'blue',attrs=['bold'])))
    print(("NOMBRE = ",colored(name_input, 'blue',attrs=['bold']),colored(lastname_input,'blue',attrs=['bold'])))
    print(("EDAD = ", colored(age_input,'blue',attrs=['bold'])))
    print(("ALTURA = ", colored(height_input,'blue',attrs=['bold'])))
    print(("PESO = ",colored(weight_input,'blue',attrs=['bold'])))
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

    print(("IMC = ",colored(IMC,colorIMC,attrs=['bold']), '-', colored(resIMC,colorIMC,attrs=['bold'])))

    createPatient = eval(input("¿Los datos son Correctos? y/n: "))

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
    Log_profile = name_folder+'.profile'
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

def borrarDatos():
    global state_loop
    ok = input("tomar otra muestra? y/n: ")
    if ok.lower() == "y":
        state_loop = 3
    else:
        state_loop = 2


##RECOLECTA LOS DATOS
def collect(i):
    global vx0, yaw0, pitch0, roll0, cond1
    cond1 = True
    date=datetime.datetime.now()
    i = 0
    t = 0
    conteo = TIEMPO_PRUEBA
    try:
        while i <= TIEMPO_PRUEBA:
            if (i==0.2):
                log_test = open(name_folder+'/'+"TUG"+str(date.day)+'-'+str(date.month)+'-'+str(date.year)+'_'+str(date.hour)+'.'+str(date.minute)+str(date.second)+'.tug', 'a')
            data = []
            data.append(arduino.readline())
            data = [x.replace("\r\n","") for x in data]
            for line in data:
                Type = line.split(",")
                a = Type[0]
                b = Type[1]
                c = Type[2]
                d = Type[3]
                e = Type[4]
                f = Type[5]
                g = Type[6]
                Line = (a + "," + b + "," + c + "," + d + "," + e + "," + f + "," + g +"\r\n")
                log_test.write(Line)
                #log_test.close()
                a = float(a)
                b = float(b)
                c = float(c)
                d = float(d)
                e = float(e)
                f = float(f)
                g = float(g)
                if(len(vx0)==0):
                    t = t + d
                    d = d - t
                if(len(vx0)>=1):
                    d = d -t
                d = d/1000
                limpiar()
                print(Medir)
                print(log_test.name)
                print(d)
                i = d
                vx0.append(d)
                yaw0.append(c)
                pitch0.append(a)
                roll0.append(b)
    
    except ValueError:
        #print"Error"
        #raw_input("volver a intentar? ")
        collect()

    except IndexError:
        #print"Error"
        #raw_input("volver a intentar? ")
        collect()

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


def graph():
    ani = animation.FuncAnimation(fig, collect, interval=1)
    plt.show()


#####Textos de Aviso
banner = colored(centerify('Full Axis V0.5 - Tesis TUG',80), 'white', attrs=['reverse'])
Salir = colored(centerify('Hasta la vista',80), 'green', attrs=['reverse'])



if __name__ == "__main__":
	main()








