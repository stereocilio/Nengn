#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "David Avila"
__credits__     = ["David Avila"]
__license__     = ""
__version__     = "0.1"
__maintainer__  = "David Avila"
__email__       = "davilaquezada@gmail.com"
__status__      = "Development"

from __init__ import *



class Triada(BaseWidget):
	
	def __init__(self):
		super(Triada,self).__init__('Triada')

		#Definition of the forms fields
		self._nombre		= ControlLabel('Paciente:'+' '+nombre+' '+apellido1+' '+apellido2+' | '+ 'Edad:'+' '+edad+' '+u'años')
		self._btncalib		= ControlButton('1.Calibrar')
		self._btnproc		= ControlButton('2.Protocolo')
		self._test			= ControlButton(u'3.Evaluación')
		self._testlibre		= ControlButton('* Test libre')
		self._ses1			= ControlCombo('Sesion')
		self._ses2			= ControlCombo('Sesion')
		self._ses3			= ControlCombo('Sesion')
		self._ser			= ControlLabel('Serial')
		self._cuadro1 	    = ControlImage('Image')
		self._cuadro2 		= ControlImage('Image')
		self._cuadro3 		= ControlImage('Image')
		self._axi1			= ControlImage('Image')
		self._axi2			= ControlImage('Image')
		self._axi3			= ControlImage('Image')
		self._ver 			= ControlButton('ver')
		self._panel 		= ControlDockWidget()

		self._formset = [('_nombre'),
						 ('_btncalib', '_btnproc', '_test', '_testlibre'),
						 ('_ses1','_ses2','_ses3','_ver'), 
						 ('_cuadro1', '_cuadro2', '_cuadro3'), 
						 ('_axi1','_axi2','_axi3'),('_ser')]
		self.title = ('Triada')
		#Define the window main menu using the property main menu
		self.mainmenu = [
			{ 'Archivo': [
					{'Nuevo Paciente': self.__dummyEvent},
					{'Buscar Paciente': self.__dummyEvent},
					'-',
					{'Salir': self.__dummyEvent}
				]
			},
			{ 'Opciones': [
					{'Calibrar': self.__dummyEvent},
					'-',
					{'Modificar': self.__dummyEvent}
				]
			},
			{ 'Ayuda': [
					{'Ayuda': self.__dummyEvent},
					{'Acerca de Triada': self.__dummyEvent}
				]
			}
		]



		###10750586

	def __dummyEvent(self):
		print ("Menu option selected")


##################################################################################################################
##################################################################################################################
##################################################################################################################

nombre = u'David'
apellido1 = u'Ávila'
apellido2 = u'Quezada'
edad = '24'

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( Triada )
