import argparse
import sys

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import json


parser = argparse.ArgumentParser(description="Does some awesome things.")
parser.add_argument('message', type=str, help="pass a message into the script")
args = parser.parse_args(sys.argv[1:])

data = []

New_data=[]
dt=[]

with open(args.message) as json_file:
    data = json.load(json_file)

def graph(grid,d_tiempo):

    plt.switch_backend('TkAgg') #default on my system

    f = plt.figure(num=args.message, figsize=(20,15))
    mng = plt._pylab_helpers.Gcf.figs.get(f.number, None)
    print(New_data)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.title(args.message)

    if grid == 1:
        tempo = d_tiempo
        tempo_init = tempo[0]
        tempo_end = tempo[-1]


    gs1 = GridSpec(4, 1)
    gs1.update(left=0.05, right=0.95, wspace=0.5, hspace=0.3, bottom=0.08)

    ax1 = plt.subplot(gs1[0, :])
    ax1.grid()
    ax1.set_ylabel('Pitch',fontsize=8)
    if grid ==1:
        L1 = ax1.plot(d_tiempo,New_data['pitch'])
    else:
        L1 = ax1.plot(d_tiempo,data['pitch'])
     
    ax2 = plt.subplot(gs1[1, :])
    ax2.grid()
    ax2.set_ylabel('Roll',fontsize=8)
    if grid ==1:
        L1 = ax2.plot(d_tiempo,New_data['roll'])
    else:
        L1 = ax2.plot(d_tiempo,data['roll'])


    ax3 = plt.subplot(gs1[2, :]) 
    ax3.grid()
    ax3.set_ylabel('Yaw',fontsize=8)
    if grid ==1:
        L1 = ax3.plot(d_tiempo,New_data['yaw'])
    else:
        L1 = ax3.plot(d_tiempo,data['yaw'])

    ax4 = plt.subplot(gs1[3, :]) 
    ax4.grid()
    ax4.set_ylabel('Tiempo',fontsize=8)
    if grid ==1:
        L1 = ax4.plot(d_tiempo,New_data['ledblue'])
        L2 = ax4.plot(d_tiempo,New_data['ledred'])
    else:
        L1 = ax4.plot(d_tiempo,data['ledblue'])
        L2 = ax4.plot(d_tiempo,data['ledred'])


    plt.show()

def find_nearest(array,values):
    idx = np.abs(np.subtract.outer(array, values)).argmin(0)
    return idx

def corte(init_cut,end_cut,a,b,c,d,e,f,g,h,i):
    a=a[init_cut:end_cut]
    b=b[init_cut:end_cut]
    c=c[init_cut:end_cut]
    d=d[init_cut:end_cut]
    e=e[init_cut:end_cut]
    f=f[init_cut:end_cut]
    g=g[init_cut:end_cut]
    h=h[init_cut:end_cut]
    i=i[init_cut:end_cut]
    datos={'roll':a,'pitch':b,'yaw':c, 'X':d, 'Y':e, 'Z':f,'time':g, 'ledblue':h, 'ledred':i}
    return datos

def reset_tempo(var_in,var_out):
    uni = var_in[0]
    for t in range(0,len(var_in)):
        var_out.append(round((var_in[t]-uni),3))
    return var_out





graph(0,data['time'])

init_cut = float(input("tiempo inicial: "))
init_cuty = find_nearest(data['time'],init_cut)
end_cut = float(input("tiempo final: "))
end_cuty = find_nearest(data['time'],end_cut)
New_data=corte(init_cuty,end_cuty,data['pitch'],data['roll'],data['yaw'],data['X'],data['Y'],data['Z'],data['time'],data['ledblue'],data['ledred'])
data = []
print(data)
data = New_data
print(data)
dt = reset_tempo(New_data['time'],dt)
graph(0,dt)
