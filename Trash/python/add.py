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
		self._pacienten		= ControlText()
		self._rut			= ControlText()
		self._nombre		= ControlText()
		self._apellido1		= ControlText()
		self._appellido2	= ControlText()
		self._dia			= ControlCombo(u'día')
		self._mes			= ControlCombo('mes')
		self._ano			= ControlCombo(u'año')



		self._dia.addItem[('Portugal', 'pt')]

		self._formset = [('_dia')]

if __name__ == "__main__":	 pyforms.startApp( Triada )
