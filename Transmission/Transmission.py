from matplotlib import cm

from input import *
from subprocess import PIPE, run
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def generate_transmission_input(gamma, input_file="H300_ref.in"):
    basename = ntpath.basename(input_file)
    name = os.path.splitext(basename)[0]

    with open(input_file, "r") as f:
        contents = f.readlines()

    settings = "0.0 " + str(gamma) + " 0.001 0 100"
    contents.insert(236, settings)
    contents.insert(248, settings)

    with open(str(name) + "_" + str(gamma) + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

def all_input_files(start, end, points):
    array = np.linspace(start, end, points)
    for i in array:
        number = round(i, 4)
        generate_transmission_input(number)

def run_input_files(start, end, points):
    array = np.linspace(start, end, points)
    for i in array:
        number = round(i, 4)
        filename = "H300_ref" + "_" + str(number)
        run_transmission(filename)

def run_transmission(inputFilename):
    command = "(cd ../Plato/bin && ./tb1 ../../Transmission/" + inputFilename + ")"
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

def get_energy_gamma_transmission(start, end, points, input_file="H300_ref.in"):
    basename = ntpath.basename(input_file)
    name = os.path.splitext(basename)[0]
    gamma = []
    energy = None
    transmission = None

    array = np.linspace(start, end, points)
    for i in array:
        gamma.append(i)
        if i == start:
            continue
        number = round(i, 4)
        file = str(name) + "_" + str(number) + "_trans.csv"
        ds = pd.read_csv('./csv4/' + file, sep=',', header=0)

        if energy is None:
            energy = np.array(ds["E(Ry)"])
        if transmission is None:
            transmission = np.zeros((len(energy), 1))
        column = np.resize(np.array(ds[" 1 - 2"]), (len(energy), 1))
        transmission = np.append(transmission, column, axis=1)

    return energy, np.array(gamma), transmission


def get_energy_gamma_transmission_XYZ(start, end, points, input_file="H300_ref.in"):
    X = []
    Y = []
    Z = []
    array = np.linspace(start, end, points)
    for i in array:
        basename = ntpath.basename(input_file)
        name = os.path.splitext(basename)[0]
        number = round(i, 4)
        file = str(name) + "_" + str(number) + "_trans.csv"
        ds = pd.read_csv('./Transmission/csv4/' + file, sep=',', header=0)
        for j in range(len(np.array(ds["E(Ry)"]))):
            X.append(i)
            Y.append(np.array(ds["E(Ry)"], dtype=float)[j])
            Z.append(np.array(ds[" 1 - 2"], dtype=float)[j])

    return np.array(X), np.array(Y), np.array(Z)

def get_energy_gamma_transmission_tuple(start, end, points, divide, input_file="H300_ref.in"):
    XYZ = []
    for i in range(start, end, points):
        basename = ntpath.basename(input_file)
        name = os.path.splitext(basename)[0]
        file = str(name) + "_" + str(i / divide) + "_trans.csv"
        ds = pd.read_csv(file, sep=',', header=0)
        for j in range(len(np.array(ds["E(Ry)"]))):
            entry = [i, np.array(ds["E(Ry)"], dtype=float)[j], np.array(ds[" 1 - 2"], dtype=float)[j]]
            XYZ.append(entry)

    return XYZ



if __name__ == '__main__':
    x_ticks = [0, 0.5, 1, 1.5, 2]
    y_ticks = [-1, -0.5, 0, 0.5, 1]

    plt.rcParams.update({'font.size': 10})
    energy, gamma, transmission = get_energy_gamma_transmission(0, 2, 667)
    energy, gamma = np.meshgrid(gamma, energy)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(energy, gamma, transmission, rstride=1, cstride=1, cmap='inferno', linewidth=0, antialiased=True)
    fig.colorbar(surf, ax=ax, shrink=0.4, aspect=15, pad=0.15, fraction=0.05)
    ax.view_init(elev=15., azim=-25)
    ax.set_ylabel('Energy (Ry)')
    ax.set_xlabel('Gamma')
    ax.set_zlabel('Transmission')
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    plt.show()

