import serial
import serial.tools.list_ports
from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import time
import json
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import datetime

intento_error = 0

window = Tk()

window.title("FullAxis Gui")

window.geometry('600x400')




lbl = Label(window, text="Tipo de prueba: ")
lbl.grid(column=0, row=0)
combo = Combobox(window, width=10)
combo['values']= ("Marcha", "TUG", "Unipodal","cabeza")
combo.current(0)
combo.grid(column=1, row=0)


lbl = Label(window, text="Prueba N: ")
lbl.grid(column=0, row=1)
n_prueba = Entry(window,width=10)
n_prueba.grid(column=1, row=1)
n_prueba.focus()

 

lbl = Label(window, text="Duración: ")
lbl.grid(column=0, row=2)
var_time =IntVar()
var_time.set(20)
spin = Spinbox(window, from_=0, to=120, width=10,textvariable=var_time)
spin.grid(column=1,row=2)


style = Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='red')
progress_var = DoubleVar() 
bar = Progressbar(window,  variable=progress_var, length=100, style='black.Horizontal.TProgressbar')
bar.grid(column=0, row=5)



def conectar():
	global arduino
	global index
	global prueba
	try:
		n_prueba.configure(state=DISABLED)
		combo.configure(state=DISABLED)

		index = int(n_prueba.get())
		prueba=combo.get()
		print(prueba)
		spin.configure(state=DISABLED)
		port = list(serial.tools.list_ports.comports())
		device = port[0]
		arduino = serial.Serial(device.device, 115200, timeout=1.)
		btn.configure(text="calibrando",state=DISABLED)
		medir(1)

	except ValueError:
		messagebox.showwarning('Error', 'debe poner un digito')
		reset()



def desconectar():
	arduino.close()
	progress_var.set(0)
	reset()


def medir(modo=0):
	global intento_error
	global datos
	try:
		TIEMPO_PRUEBA = int(spin.get())
		if modo==1:
			progress1 = 0
			conteo = 5
			for t in range(5):
				i = 0
				progress1= progress1+20

				progress_var.set(progress1)
				window.update_idletasks()
				while i <= conteo:
					data = [""]
					data[0]=(str(arduino.readline()))
					data = [x.replace("\\r\\n","") for x in data]
					data = [x.replace("b'","") for x in data]
					data = [x.replace("\'","") for x in data]
					print(data[0])
					for line in data:
						Type = line.split(",")
						RollC1 = (float(Type[0]))
						PitchC1 = -(float(Type[1]))
						YawC1 = float(Type[2])
						X_sensor2 = float(Type[3])
						Y_sensor2 = -(float(Type[4]))
						Z_sensor2 = -(float(Type[5]))
						tiempoSegundos = int(Type[6])
						stateLed = int(Type[7])
						stateLedRED = int(Type[8])
					i = i+1



			if((bar['value'])==100):
				btn.configure(text="desconectar",state=NORMAL, command=desconectar)
				btn1.configure(text="Comenzar",state=NORMAL, command=medir)
				intento_error = 0


		if modo==0:
			btn1.configure(text="Comenzar",state=DISABLED)
			btn.configure(text="desconectar",state=DISABLED)
			progress_var.set(0)
			style.configure("black.Horizontal.TProgressbar", background='green')
			window.update_idletasks()
			i = 0
			progress2_unit = 100/(TIEMPO_PRUEBA)
			progress2=0
			datos={'roll':[],'pitch':[],'yaw':[],'X':[],'Y':[],'Z':[],'time':[],'ledblue':[],'ledred':[]}
			while i <= TIEMPO_PRUEBA:
				data = []
				data =[""] #Existe el error que si se desconecta al medir no entra en error
				data[0]=(str(arduino.readline()))
				data = [x.replace("\\r\\n","") for x in data]
				data = [x.replace("b'","") for x in data]
				data = [x.replace("\'","") for x in data]
				tiempoSegundos = 0
				for line in data:
					Type = line.split(",")
					RollC1 = (float(Type[0]))
					PitchC1 = -(float(Type[1]))
					YawC1 = float(Type[2])
					X_sensor2 = float(Type[3])
					Y_sensor2 = -(float(Type[4]))
					Z_sensor2 = -(float(Type[5]))
					if datos['time'] == []:
						corrector = int(Type[6])
					tiempoSegundos = ((int(Type[6]))-corrector)
					stateLed = int(Type[7])
					stateLedRED = int(Type[8])
					datos['roll'].append(RollC1)
					datos['pitch'].append(PitchC1)
					datos['yaw'].append(YawC1)
					datos['X'].append(X_sensor2)
					datos['Y'].append(Y_sensor2)
					datos['Z'].append(Z_sensor2)
					datos['time'].append(tiempoSegundos)
					datos['ledblue'].append(stateLed)
					datos['ledred'].append(stateLedRED)
				i = tiempoSegundos/1000
				progress2=(i*100)/TIEMPO_PRUEBA
				progress_var.set(progress2)
				window.update_idletasks()
			with open(str(index)+'.'+prueba, 'w') as json_file:
				json.dump(datos, json_file)
			desconectar()

	except ValueError:
		if intento_error<= 3:
			intento_error=intento_error+1
			reset_arduino()
			if modo == 1:
				medir(1)
			else:	
				medir(0)
		else:
			messagebox.showwarning('Error de Comunicación', 'Verifique el equipo')
			reset()

	except IndexError:
		if intento_error<= 3:
			intento_error=intento_error+1
			reset_arduino()
			if modo == 1:
				medir(1)
			else:
				medir(0)
		else:
			messagebox.showwarning('Error de Comunicación', 'Verifique el equipoff')
			reset()
	except TypeError:
		if intento_error<= 3:
			intento_error=intento_error+1
			reset_arduino()
			if modo == 1:
				medir(1)
			else:
				medir(0)
		else:
			messagebox.showwarning('Error de Comunicación', 'Verifique el equipo')
			reset()


def reset_arduino():
	global arduino
	arduino.setDTR(False)
	arduino.flushInput()
	arduino.setDTR(True)

def reset():
	global arduino
	progress_var.set(0)
	spin.configure(state=NORMAL)
	combo.configure(state=NORMAL)
	n_prueba.configure(state=NORMAL)
	btn1.configure(text="Comenzar",state=DISABLED, command=medir)
	btn.configure(text="Conectar",state=NORMAL, command=conectar)
	try:
		graph()
	except:
		pass
	try:
		arduino.setDTR(False)
		time.sleep(1)
		arduino.flushInput()
		arduino.setDTR(True)
	except:
		pass



def graph():

	plt.switch_backend('TkAgg') #default on my system
	print(('Backend: {}'.format(plt.get_backend())))
	f = plt.figure(num=str(index)+'.'+prueba, figsize=(20,15))
	mng = plt._pylab_helpers.Gcf.figs.get(f.number, None)
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.title(str(index)+'.'+prueba)

	gs1 = GridSpec(7, 1)
	gs1.update(left=0.05, right=0.95, wspace=0.5, hspace=0.3, bottom=0.08)

	ax1 = plt.subplot(gs1[0, :])
	ax1.grid()
	ax1.set_ylabel('Roll',fontsize=8)
	L1 = ax1.plot(datos['time'],datos['roll'])

	ax2 = plt.subplot(gs1[1, :])
	ax2.grid()
	ax2.set_ylabel('Pitch',fontsize=8)
	L2 = ax2.plot(datos['time'],datos['pitch'])

	ax3 = plt.subplot(gs1[2, :])
	ax3.grid()
	ax3.set_ylabel('Yaw',fontsize=8)
	L3 = ax3.plot(datos['time'],datos['yaw'])

	ax4 = plt.subplot(gs1[3, :])
	ax4.grid()
	ax4.set_ylabel('X',fontsize=8)
	L4 = ax4.plot(datos['time'],datos['X'])

	ax5 = plt.subplot(gs1[4, :])
	ax5.grid()
	ax5.set_ylabel('Y',fontsize=8)
	L5 = ax5.plot(datos['time'],datos['Y'])

	ax6 = plt.subplot(gs1[5, :])
	ax6.grid()
	ax6.set_ylabel('Y',fontsize=8)
	L6 = ax6.plot(datos['time'],datos['Z'])

	ax7 = plt.subplot(gs1[6, :])
	ax7.grid()
	ax7.set_ylabel('LED_TIME',fontsize=8)
	L7 = ax7.plot(datos['time'],datos['ledblue'])
	L8 = ax7.plot(datos['time'],datos['ledred'])

	date=datetime.datetime.now()
	name = (str(index)+'_'+prueba+str(date.day)+'-'+str(date.month)+'-'+str(date.year)+'_'+str(date.hour)+':'+str(date.minute)+':'+str(date.second)+'.png')
	plt.savefig(name, bbox_inches='tight')
	plt.show()


btn = Button(window, text="Conectar", command=conectar)
btn.grid(column=0, row=3)

btn1 = Button(window, state=DISABLED, text="Comenzar", command=medir)
btn1.grid(column=1, row=3)


def printt():
	print("hola")

frame = Frame(window)	
frame.bind("<b>", printt)

window.mainloop()
