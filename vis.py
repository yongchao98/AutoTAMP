from gurobipy import *
import numpy as np
from collections import namedtuple
import time
import pickle
import pypoman as ppm
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

def vis(plots, PWLs, limits=None, equal_aspect=True):
    print(PWLs)
    plt.rcParams["figure.figsize"] = [6.4, 6.4]
    plt.rcParams['axes.titlesize'] = 20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis('off')

    vertices = []
    for plot in plots:
        #print('plot: ', plot)
        for A, b in plot[0]:
            vs = ppm.duality.compute_polytope_vertices(A, b)
            vertices.append(vs)
            ppm.polygon.plot_polygon(vs, color = plot[1], alpha=1.)
            if plot[2] != 'wall':
                plt.text((-b[0] + b[1])/2-0.32, (-b[2] + b[3])/2-0.1, plot[2],color = (0.6,0.6,0.6), fontsize=12, fontweight='bold')

    if limits is not None:
        plt.xlim(limits[0])
        plt.ylim(limits[1])
    else:
        vertices = np.concatenate(vertices, axis=0)
        xmin, ymin = vertices.min(axis=0)
        xmax, ymax = vertices.max(axis=0)
        plt.xlim([xmin - 0.1, xmax + 0.1])
        plt.ylim([ymin - 0.1, ymax + 0.1])

    if equal_aspect:
        plt.gca().set_aspect('equal', adjustable='box')

    if PWLs is None or PWLs[0] is None:
        plt.show()
        return

    if len(PWLs) <= 4:
        colors = ['k', np.array([153,0,71])/255, np.array([6,0,153])/255, np.array([0, 150, 0])/255]
    else:
        cmap = plt.get_cmap('tab10')
        colors = [cmap(i) for i in np.linspace(0, 0.85, len(PWLs))]

    for i in range(len(PWLs)):
        PWL = PWLs[i]
        ax.plot([P[0][0] for P in PWL], [P[0][1] for P in PWL], '-', color = colors[i])
        ax.plot(PWL[-1][0][0], PWL[-1][0][1], '*', color = colors[i])
        ax.plot(PWL[0][0][0], PWL[0][0][1], 'o', color = colors[i])
    plt.show()
