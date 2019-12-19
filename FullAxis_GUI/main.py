#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:        main.py (Python 3.x).
# description: Software para la medición de IMU 9DOF
# purpose:     Analisis de la marcha y movimientos corporales
#              mediante IMU
# author:      David Avila Quezada
#
#------------------------------------------------------------

'''FullAxis: Software para la medición de los movimientos corporales'''
   
__author__ = 'Debaq'
__title__= 'FullAxis'
__date__ = '12/19'
__version__ = '0.4'
__license__ = 'MIT'

#Librerias Necesarias
#Tkinter para dibujar el Gui, PIL para trabajar con img
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox

#Librerias para trabajr numeros y datos importados
import numpy as np
import csv 
import pandas

#Libreria para utilizar parametros especificos del sistema
import os
import sys
import setproctitle
import shutil
sys.path.insert(1, 'config/') #se señala carpeta donde se encuentran librerias propias

#Librerias propias para manejar componentes externos, principalmente configuraciones
import languaje as lang
import setting as stt
import tools 

#Libreria para controlar gráficos, es necesario analisar si se puede enviar a libreria propia 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Ellipse
import matplotlib.animation as animation
from matplotlib.text import OffsetFrom
from matplotlib.gridspec import GridSpec

#Librerias para comunicación Serial y su uso 
import serial
import serial.tools.list_ports
import time

#Establece nombre en gestor de procesos
setproctitle.setproctitle('FullAxis')


#Establece Idioma seteado
LANG=0
path=".tmp"


def delete_window(save=True):
	if save:
		q=messagebox.askyesnocancel(message="¿Desea guardar antes de salir?", title="FullAxis")
		if q==True:
			messagebox.showinfo(message="Registros Guardados Exitosamente", title="FullAxis")		
			root.destroy()
		if q==False:
			print("no se guardo nada")
			raise SystemExit
			root.destroy()
	else:
		print("no se guardo nada")
		raise SystemExit
		root.destroy()

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=BOTTOM, anchor=W, state=NORMAL):
      Frame.__init__Frame(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var, state=state)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

class Lelitxipawe:
	'''
	Clase principal de la Ventana
	'''
	def __init__(self, master=None): #Se inicia la ventana con sus caracteristicas predeterminadas
		self.root = master
		self.root.config(background='white')#Color de fondo
		self.root.update_idletasks()
		#self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()
		self.w,self.h = 1280,720
		self.root.geometry("%dx%d+0+0" % (self.w, self.h))
		self.root.minsize(self.w, self.h)#Tamaño minimo de la ventana
		#self.root.maxsize(self.w, self.h)#Tamaño minimo de la ventana
		self.root.attributes('-zoomed', True)
		#self.root.overrideredirect(True)
		self.root.call('wm', 'iconphoto', self.root._w, ImageTk.PhotoImage(Image.open('resources/icon.png')))#Icono de la ventana
		#declarar Variables
		self.che()
		self.app()

	def che(self, ini=True):#Variables del individuo
		if ini:
			self.ID = IntVar(value=1)
			self.Name   = StringVar("")
			self.LastName   = StringVar("")
			self.edad = IntVar(value=99)
			self.ID_read = IntVar()
			self.NameLast_read = StringVar()
			self.edad_read = IntVar()
		else:
			#try:
			self.ID.set(value=1)
			self.Name.set("")
			self.LastName.set("")
			self.edad.set(value=99)
			read = tools.read_profile(path)
			NameLast = read['nombre']+" "+read['apellidos']
			self.ID_read.set(read['ID'])
			self.NameLast_read.set(NameLast)
			self.edad_read.set(read['edad'])
		#	except FileNotFoundError:
		#		messagebox.showinfo(message="Error al Crear el perfil", title="FullAxis")

	def app(self): #Estructura de la ventana
		self.txokiñ()
		self.ñizol()
		self.retron()
		self.üitun()
		self.wirin()
		self.wirin_epu()

	def ñizol(self): #Menú principal
		menu = Menu(self.root)
		self.root.config(menu=menu)
		file = Menu(menu, tearoff=0)
		file.add_command(label="Abrir usuario")
		file.add_command(label="Nuevo usuario", command=self.we_kakon)
		file.add_command(label="Importar usuario", command=self.abrir)
		file.add_command(label="Exportar usuario", command=self.abrir)
		file.add_command(label="Cerrar usuario")
		file.add_separator()
		file.add_command(label="Imprimir...")
		file.add_separator()
		file.add_command(label="Salir",command=lambda:delete_window(True))
		file.add_command(label="Salir sin guardar",command=lambda:delete_window(False))
		menu.add_cascade(label="Archivo", menu=file)
		edit = Menu(menu, tearoff=0)
		edit.add_command(label="Nueva Prueba", command=self.llitulün)
		edit.add_command(label="Borrar Prueba")
		edit.add_separator()
		edit.add_command(label="Exportar resultados a csv")
		edit.add_separator()
		edit.add_command(label="Abrir prueba suelta")
		menu.add_cascade(label="Editar", menu=edit)
		help = Menu(menu, tearoff=0)
		help.add_command(label="Ayuda")
		help.add_separator()
		help.add_command(label="Acerca de nosotros",)
		menu.add_cascade(label="Ayuda", menu=help)

	def txokiñ(self):#Marcos y estructura
		#Configuración de los Frames, proporciones en setting.py variable size_frame
		size_frame=stt.size_screen(self.w,self.h)

		self.frame_quick = Frame(bd=1,relief="sunken") ##crea la caja superior
		self.frame_contenido = Frame(bd=1, bg="white",relief="sunken") ##crea la caja derecha
		self.frame_info = Frame(bd=1,relief="sunken") ##crea la caja inferior
		frame_command = Frame(bd=1,relief="sunken") ##crea la caja izquierda
		#se ubican los frames en la ventana principal
		self.frame_quick.place(	relx=size_frame['up'][0], rely=size_frame['up'][1], 
								relwidth=size_frame['up'][2], relheight=size_frame['up'][3])
		self.frame_contenido.place(	relx=size_frame['der'][0], rely=size_frame['der'][1], 
									relwidth=size_frame['der'][2], relheight=size_frame['der'][3])
		frame_command.place(	relx=size_frame['izq'][0], rely=size_frame['izq'][1], 
									relwidth=size_frame['izq'][2], relheight=size_frame['izq'][3])
		self.frame_info.place(	relx=size_frame['down'][0], rely=size_frame['down'][1], 
								relwidth=size_frame['down'][2], relheight=size_frame['down'][3])

		frame_paned_up = Frame(frame_command)
		paned_data = PanedWindow(frame_paned_up, orient=VERTICAL)
		self.frame_data = Frame(paned_data)
		self.frame_registros = Frame(paned_data)
		self.frame_data.pack(side = TOP)
		self.frame_registros.pack(side = TOP)
		paned_data.add(self.frame_data,minsize=60)
		paned_data.add(self.frame_registros, minsize=30)
		paned_data.pack(fill = BOTH, expand = True) 
		paned_data.configure(sashrelief = RAISED)
		#paned_data.configure(self.frame_data, height=.2)
		frame_paned_up.place(relwidth=1, relheight=0.5)
		
		frame_paned_down = Frame(frame_command)
		paned_result = PanedWindow(frame_paned_down, orient=VERTICAL)
		self.frame_other = Frame(paned_result, bg="lightblue")
		self.frame_curva = Frame(paned_result, bg="white")
		self.frame_other.pack(side=TOP)
		self.frame_curva.pack(side=TOP)
		paned_result.add(self.frame_other)
		paned_result.add(self.frame_curva)
		paned_result.pack(fill=BOTH, expand=True)
		paned_result.configure(sashrelief=RAISED)
		frame_paned_down.place(rely=0.5, relwidth=1, relheight=0.5)
		#self.frame_other.place(rely =1/2, relwidth=1, relheight=1/6)
		#self.frame_curva.place(rely = 2/3, relwidth=1, relheight=1/3)

	def üitun(self): #Datos del sujeto seleccionado
		frame = LabelFrame(self.frame_data,  text="Datos:", padx=2, pady=2)
		labels =["ID","Nombre","Edad","IMC"]
		for i in enumerate(labels):
			label = Label(frame, text=i[1]).grid(column=0 , row=i[0], sticky="w", padx=5)
		for i in range(4):
			label = Label(frame, text=":").grid(column=1 , row=i, sticky="w", padx=5)

		datos = [self.ID_read,self.NameLast_read, self.edad_read, "20"]
		for i in enumerate(datos):
			label = Label(frame, textvariable=i[1]).grid(column=2 , row=i[0], sticky="w", padx=3)

		button = Button(frame, text="Modificar").grid(column=1,row=6, columnspan=3, sticky=W)
		frame.pack(fill=BOTH, expand=1,padx=2, pady=2)

	def wirin(self):#se dibujan los gráficos, pantalla principal
		fig = self.wirikan()
		self.graphy = FigureCanvasTkAgg(fig, master=self.frame_contenido)
		self.graphy.get_tk_widget().pack(side="top",fill='both',expand=True)

	def wirin_epu(self):#Se dibujan los gráficos, zoom seleccionado
		fig = self.wirikan_select()
		self.graphy2 = FigureCanvasTkAgg(fig, master=self.frame_curva)
		self.graphy2.get_tk_widget().pack(side="top", fill="both", expand=True)

	def wirikan(self): #Graficos principales
		fig = plt.figure(figsize=(20,15))
		gs1 = GridSpec(7, 1)
		gs1.update(left=0.05, right=0.95, wspace=0.5, hspace=0.3, top=0.98, bottom=0.08)

		ax1 = plt.subplot(gs1[0:2,:])
		ax1.grid()
		ax1.set_ylabel('Roll',fontsize=8)
		ax1.xaxis.set_tick_params(labelsize=7)
		ax1.yaxis.set_tick_params(labelsize=7)

		ax2 = plt.subplot(gs1[2:4,:])
		ax2.grid()
		ax2.set_ylabel('Pitch',fontsize=8)
		ax2.xaxis.set_tick_params(labelsize=7)
		ax2.yaxis.set_tick_params(labelsize=7)

		ax3 = plt.subplot(gs1[4:6,:])
		ax3.grid()
		ax3.set_ylabel('Yaw',fontsize=8)
		ax3.xaxis.set_tick_params(labelsize=7)
		ax3.yaxis.set_tick_params(labelsize=7)

		ax4 = plt.subplot(gs1[6,:])
		ax4.grid()
		ax4.set_ylabel('Mark',fontsize=8)
		ax4.xaxis.set_tick_params(labelsize=7)
		ax4.yaxis.set_tick_params(labelsize=7)

		return fig

	def wirikan_select(self):#Graficos segundarios
		fig = plt.figure(figsize=(10,10))
		gs1 = GridSpec(1, 1)
		
		ax1 = plt.subplot(gs1[0:2,:])
		ax1.grid()
		plt.xticks(fontsize=6, rotation=90)
		plt.yticks(fontsize=6, rotation=90)
		
		return fig

	def wirikan_2(x_vec,y1_data,line1,identifier='',pause_time=0.01):#Algo que borrar si no se encuentra uso
		if line1==[]:
			plt.ion()
			#fig = plt.figure(figsize=(13,6))
			#ax = fig.add_subplot(111)
			#line1, = ax.plot(x_vec,y1_data)
			line1, = self.ax3.plot(x_vec,y1_data)

			plt.show()
			#self.graphy.draw()

		#line1.set_data(x_vec,y1_data)

		plt.pause(pause_time)

		return line1

	def we_kakon(self):#Ventana para ingresar nuevo sujeto
   
		#Crear Ventana
		self.kakon = Toplevel(takefocus=True)
		self.kakon.focus_force()
		self.kakon.attributes("-topmost", True)
		self.kakon.title("Nuevo registro")
		self.kakon.minsize(400, 200)
		self.kakon.maxsize(400, 200)
		#self.kakon.bind("<FocusOut>",self.focus_kakon)


		#trazas para evaluar cambio
		self.Name.trace('w', self.ver_new_user)
		self.LastName.trace('w', self.ver_new_user)

		#Cargar Imagen	
		#new_user = Image.open('resources/new_user.png')	
		#new_user = PhotoImage(new_user)  
	
		#Declaro Widget y los cargo a a la ventana
		#Sobre la ventana cargo dos frames, 
		#frame_data: contiene los datos que se vana a cargar para crear el perfil
		#frame_button: contiene los botones "crear y cancelar"
		frame_data = Frame(self.kakon)
		frame_button = Frame(self.kakon)
		#declaro las labels dentro del frame_data:

		labels =["ID","Nombre","Apellidos","Edad"]
		for i in enumerate(labels):
			label = Label(frame_data, text=i[1]).grid(column=0 , row=i[0], sticky="w", padx=5)
		for i in range(4):
			label = Label(frame_data, text=":").grid(column=1 , row=i, sticky="w", padx=5)
		
		#declaro los entry dentro del frame_data:
		entry_ID = Entry(frame_data, width=10, textvariable=self.ID).grid(column=2, row=0)
		entry_name = Entry(frame_data, width=10, textvariable=self.Name)
		entry_name.grid(column=2, row=1)
		entry_name.focus()
		entry_lastName = Entry(frame_data, width=10, textvariable=self.LastName).grid(column=2, row=2)
		entry_edad = Entry(frame_data, width=10, textvariable=self.edad).grid(column=2, row=3)
		btn_cancelar = Button(frame_button, text="Cancelar",command=self.kakon.destroy)
		btn_cancelar.grid(column=0, row=0)
		self.btn_crear = Button(frame_button, text="Crear",state=DISABLED,command=self.new_user)
		self.btn_crear.grid(column=1, row=0)

		#le paso pack() a los frames
		#imagen1.pack(side=TOP, fill=BOTH, expand=True)
		frame_data.pack(side=TOP, fill=BOTH, expand=True, anchor="center")
		frame_button.pack(side=TOP, fill=BOTH, expand=True, anchor="center")

	def ver_new_user(self, *args):#función para activar o desactivar botón
		#se cambia la propiedad del boton crear_nuevo
		#nota: si se usa pack() no funciona button.config()
		name=self.Name.get()
		lastname=self.LastName.get()
		try:
			if ((name and lastname)  != ("")):
				self.btn_crear.config(state=NORMAL)
			else:
				self.btn_crear.config(state=DISABLED)
		except:
			pass

	def new_user(self):#Función para crear nuevo usuario
		#Invoco funciones externas:
		try:
			tools.new_user(path,self.ID.get(),self.Name.get(),self.LastName.get(),self.edad.get()) 
			self.kakon.destroy()
			self.che(False)		
			messagebox.showinfo(message="Creado Correctamente", title="FullAxis")
		except:
			messagebox.showinfo(message="Error al Crear el perfil", title="FullAxis")

	#def focus_kakon(self,event):
	#	self.kakon.focus_force()

	def abrir(self):#Función para abrir sujetos guardados
		file = filedialog.askopenfilename(parent=self.root, initialdir = "~/",
										  title = "Seleccione el archivo",
										  filetypes = [("Datos FullAxis","*.fxs")
										 			  ,("all files","*.*")])
		return(file)

	def retron(self): #árbol de pruebas
		frame=LabelFrame(self.frame_registros, text="Historial", padx=5, pady=5)
		self.treeview = ttk.Treeview(frame)
		self.treeview.pack(fill=BOTH, expand=True)
		frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
		video = self.treeview.insert("",END, text="Video", open=False)
		acc = self.treeview.insert("",END, text="IMU", open=True)
		estb = self.treeview.insert("",END, text="Estabilómetro",open=False)


		self.pruebas_voculo = ["Espontáneo", "Calórica", "VHIT", "MPP"]
		self.pruebas_acc  = ["Marchas", "dTUG", "Unipodal","Romberg", "Fukuda"]
		self.pruebas_estb = ["SOT", "Max. desplazamiento", "RV"]

		self.esponaneo = self.treeview.insert(video,END, text=self.pruebas_voculo[0])
		self.calorica = self.treeview.insert(video,END, text=self.pruebas_voculo[1])
		self.VHIT = self.treeview.insert(video,END, text=self.pruebas_voculo[2])
		self.MPP = self.treeview.insert(video,END, text=self.pruebas_voculo[3])

		self.Marchas = self.treeview.insert(acc,END, text=self.pruebas_acc[0])
		self.dTUG = self.treeview.insert(acc,END, text=self.pruebas_acc[1])
		self.Unipodal = self.treeview.insert(acc,END, text=self.pruebas_acc[2])
		self.Romberg = self.treeview.insert(acc,END, text=self.pruebas_acc[3])
		self.Fukuda = self.treeview.insert(acc,END, text=self.pruebas_acc[4])

		self.SOT = self.treeview.insert(estb,END, text=self.pruebas_estb[0])
		self.despl = self.treeview.insert(estb,END, text=self.pruebas_estb[1])
		self.RV = self.treeview.insert(estb,END, text=self.pruebas_estb[2])
		
		self.treeview.tag_bind(self.Marchas, "<<TreeviewSelect>>",
								self.item_selected)

	def llitulün(self):#Ventana de crear bateria de pruebas
		#Crear Ventana
		self.llitulün = Toplevel(takefocus=True)
		self.llitulün.focus_force()
		self.llitulün.attributes("-topmost", True)
		self.llitulün.title("Nueva Prueba")
		self.llitulün.minsize(400, 200)
		self.llitulün.maxsize(400, 200)

		frame_data = Frame(self.llitulün)
		frame_data_IMU = LabelFrame(frame_data, text="IMU", padx=5, pady=5)
		frame_data_postu = LabelFrame(frame_data, text="Estabilometría", padx=5, pady=5)
		frame_data_oculo = LabelFrame(frame_data, text="Video-oculometría", padx=5, pady=5)
		frame_button = Frame(self.llitulün, padx=10, pady=5)
		label = Label(self.llitulün, text="Seleccione batería de pruebas a realizar").pack()
		
		frame_data.pack()
		frame_button.pack(fill=BOTH)

		
		btn_cancelar = Button(frame_button, text="Cancelar",command=self.llitulün.destroy)
		btn_cancelar.pack(side=RIGHT)
		self.btn_crear_pruebas = Button(frame_button, text="Crear",state=DISABLED)
		self.btn_crear_pruebas.pack(side=RIGHT)

		check_IMU = Checkbar(frame_data_IMU, self.pruebas_acc)
		check_postu = Checkbar(frame_data_postu, self.pruebas_estb, state=DISABLED)
		check_oculo = Checkbar(frame_data_oculo, self.pruebas_voculo, state=DISABLED)
		check_oculo.pack()
		check_postu.pack()
		check_IMU.pack()
		frame_data_oculo.pack(side=LEFT, fill=Y)
		frame_data_IMU.pack(side=LEFT, fill=Y)
		frame_data_postu.pack(side=LEFT, fill=Y)


	def item_selected(self, event):
		"""Item seleccionado."""
		print("Seleccionado.")

if __name__ == '__main__':
	path_actual = os.getcwd()
	try:
		os.mkdir(path)
	except FileExistsError:
		shutil.rmtree(path)
		os.mkdir(path)

	root = Tk()
	root.protocol("WM_DELETE_WINDOW", delete_window)
	#root.bind("<Destroy>", destroy)

	my_gui = Lelitxipawe(master=root)
	my_gui.root.wm_title("FullAxis V.4")
	root.mainloop()
	#shutil.rmtree(path)
	#raise SystemExit



#------------------------------------------------------------
###NOTAS:
#I2c al perder electricidad se pierden las direcciones de los otrso dispsitivos 
#IDEAS:
#Encriptación de los documentos con contraseña del usuario
#Se pueden almacenar las variables que contienen funciones en una lista y esta lista se puede iterar con un for para modificarle algo?
