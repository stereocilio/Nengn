import pandas as pd
import json
import datetime
import tarfile
from os import remove


def new_user(path,ID,name,lastname,edad):
	#print(ID,name,lastname,edad)

	date=datetime.datetime.now()
	FC = str(date.day)+'-'+str(date.month)+'-'+str(date.year)
	profile = {	'ID'		:	ID,
				'FC'		: 	FC,
				'nombre'	:	name,
				'apellidos'	:	lastname,
				'edad'		:	edad,
				'test'		:	[]
			  }

	path_profile = path+"/"+'PROFILE.info'
	with open(path_profile, 'w') as json_file:
				json.dump(profile, json_file)

	tar = tarfile.open(path+"/"+'temp.fxs', mode='w')
	tar.add(path_profile)
	tar.close()
	#remove(path_profile)

def save_all():
	pass


def read_profile(path):
	path_profile = path+"/"+'PROFILE.info'
	with open(path_profile) as json_file:
		data = json.load(json_file)
		return data
	