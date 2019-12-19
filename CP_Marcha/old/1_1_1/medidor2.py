import argparse
import sys

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import csv


parser = argparse.ArgumentParser(description="Does some awesome things.")
parser.add_argument('message', type=str, help="pass a message into the script")
args = parser.parse_args(sys.argv[1:])

a = []
b = []
c = []
d = []
e = []
l = []
g = []
dt = []

with open(args.message,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        a.append(float(row[0]))
        b.append(float(row[1]))
        c.append(float(row[2]))
        d.append((float(row[3]))/1000)
        e.append((float(row[4]))/1000)
        l.append(int(row[5]))
        g.append(int(row[6]))



def graph(grid,d_tiempo):

    plt.switch_backend('TkAgg') #default on my system

    f = plt.figure(num="TUG", figsize=(20,15))
    mng = plt._pylab_helpers.Gcf.figs.get(f.number, None)


    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.title("TUG con acelerometria")

    if grid == 1:
        tempo = d_tiempo
        tempo_init = tempo[0]
        tempo_end = tempo[-1]


    gs1 = GridSpec(5, 2)
    gs1.update(left=0.05, right=0.95, wspace=0.5, hspace=0.3, bottom=0.08)

    ax2 = plt.subplot(gs1[0, :])
    ax2.grid()
    ax2.set_ylabel('Lateral',fontsize=8)
    L1 = ax2.plot(d_tiempo,a)
    if grid ==1:
        plt.xticks(np.arange(tempo_init, tempo_end, step=0.5))

     
    ax3 = plt.subplot(gs1[1, :])
    ax3.grid()
    ax3.set_ylabel('Antero-posterior',fontsize=8)
    L1 = ax3.plot(d_tiempo,b)
    if grid ==1:
        plt.xticks(np.arange(tempo_init, tempo_end, step=0.5))


    ax4 = plt.subplot(gs1[2, :]) 
    ax4.grid()
    ax4.set_ylabel('Giro',fontsize=8)
    L1 = ax4.plot(d_tiempo,c)
    if grid ==1:
        plt.xticks(np.arange(tempo_init, tempo_end, step=0.5))


    ax4 = plt.subplot(gs1[3, :]) 
    ax4.grid()
    ax4.set_ylabel('RED',fontsize=8)
    L1 = ax4.plot(d_tiempo,g)
    if grid ==1:
        plt.xticks(np.arange(tempo_init, tempo_end, step=0.5))

    ax4 = plt.subplot(gs1[4, :]) 
    ax4.grid()
    ax4.set_ylabel('BLUE',fontsize=8)
    L1 = ax4.plot(d_tiempo,l)
    if grid ==1:
        plt.xticks(np.arange(tempo_init, tempo_end, step=0.5))

    plt.show()

def find_nearest(array,values):
    idx = np.abs(np.subtract.outer(array, values)).argmin(0)
    return idx

def corte(init_cut,end_cut,a,b,c,d,e,f,g):
    a=a[init_cut:end_cut]
    b=b[init_cut:end_cut]
    c=c[init_cut:end_cut]
    d=d[init_cut:end_cut]
    f=f[init_cut:end_cut]
    g=g[init_cut:end_cut]

    return a, b, c, d, e, f, g

def reset_tempo(var_in,var_out):
    uni = var_in[0]
    for t in range(0,len(var_in)):
        var_out.append(round((var_in[t]-uni),3))
    return var_out

graph(0,d)

init_cut = float(input("tiempo inicial: "))
init_cuty = find_nearest(d,init_cut)
end_cut = float(input("tiempo final: "))
end_cuty = find_nearest(d,end_cut)
a,b,c,d,e,f,g=corte(init_cuty,end_cuty,a,b,c,d,e,f,g)
dt = reset_tempo(d,dt)
graph(1,dt)
