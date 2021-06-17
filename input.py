import math
import ntpath
from datetime import datetime
import pyqtgraph
from PyQt5 import QtGui
import shlex
from atom import Atom
import os

RYDBERG = 13.605685


def lines_that_contain(string, f):  # returns the line which contains string in f
    return [line for line in f if string in line]


def lines_that_start_with(string, f):  # returns the line which contains string in f
    return [line for line in f if string in line.split()[:1]]


# returns last char which contains string in f
def get_last_char(string, file):
    array = []
    with open(file, "r") as f:
        for line in lines_that_contain(string, f):
            array.append(line.strip()[-1])
    return array


# returns lines between start and end strings
def get_lines_between(file, start, end, end_opt="second end", skip_line=True, pop_twice=False, skip=0):
    array = []
    copy = False
    with open(file, "r") as f:
        for line in f:
            if line.strip() == start:
                if skip > 0:
                    skip = skip - 1
                    continue
                start = None
                copy = True
                if skip_line:
                    next(f)
                continue
            elif line.strip() == end or line.strip() == end_opt:
                copy = False
                continue
            elif copy:
                array.append(line.strip())
    array.pop()
    if pop_twice:
        array.pop()
    return array


def get_line_number(file, string):
    line_count = 1
    with open(file, "r") as f:
        for line in f:
            if line.strip() == string:
                return line_count
            line_count += 1
    return line_count + 1


def correct_quantum(quantum):
    quantum_array = []
    for i in range(len(quantum)):
        quant_split = [int(x) for x in quantum[i].split()]
        quant_split[2] -= quant_split[1]
        quantum_array.append(quant_split)
    return quantum_array


def create_orbital_dict(file):  # returns orbitals for each element
    orb_dict = {}
    quantum_dict = {}
    elements = get_last_char("Chemical symbol           :", file)
    orbitals = get_last_char("Number of orbitals        :", file)
    assert len(elements) == len(orbitals) != 0
    for i in range(len(elements)):
        new_entry = {str(elements[i]): orbitals[i]}
        orb_dict.update(new_entry)
        quantum = get_lines_between(file, "n l m     energy     occupancy    radius",
                                    "---------------------------", "----------------", False, True, i)
        quantum = [item[:5] for item in quantum]
        quantum = correct_quantum(quantum)
        new_quantum = {str(elements[i]): quantum}
        quantum_dict.update(new_quantum)

    return orb_dict, quantum_dict


def create_all_atoms(file):  # creates orbitals for each element using .out
    array = []
    xyz = get_lines_between(file, "Atomic positions (a0):", "Total forces (Ry/a0):")
    for i in range(len(xyz)):
        xyz_split = xyz[i].split()
        new_entry = Atom(*xyz_split, i + 1)
        array.append(new_entry)
    return array


def set_attr_from_file(file, atoms):  # sets attributes to atoms from attributes.txt (skips first line)
    for i in range(len(atoms)):
        with open(file, "r") as f:
            next(f)
            for line in lines_that_start_with(atoms[i].get_symbol(), f):
                attributes = shlex.split(line)
                atoms[i].set_colour(pyqtgraph.glColor(QtGui.QColor(attributes[1])))
                atoms[i].set_radius(attributes[2])
                elem = 3
                while elem < (len(attributes)):
                    atoms[i].set_bonding(attributes[elem])
                    elem += 1


def total_orbitals(atoms, orb_dict):  # finds total number of orbitals in system
    total = 0
    for i in range(len(atoms)):
        count = orb_dict.get(atoms[i].get_symbol(), None)
        total += int(count)
    return total


def eig_arr_from_wf(file, atoms, orb_dict):  # returns 2D array with all eigenvalues split by mode
    all_modes = []
    a_mode = []
    energies = []
    total = total_orbitals(atoms, orb_dict)
    four_places = "{:.4f}"
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                energies.append(four_places.format(float(line.split()[0])))
                continue
            if i % (total + 1) == 0:
                all_modes.append(a_mode)
                a_mode = []
                energies.append(four_places.format(float(line.split()[0])))
                continue
            a_mode.append(line.strip())
    all_modes.append(a_mode)
    return all_modes, energies


# sets 2D array of eigenvalues split by mode per atom, sets orbital count and quantum dict #
def set_eig_to_atoms(atoms, orb_dict, quantum_dict, all_modes, energies):
    for i in range(len(all_modes)):
        orbital = 0
        for j in range(len(atoms)):
            mode_i = []
            count = orb_dict.get(atoms[j].get_symbol(), None)
            for _ in range(int(count)):
                mode_i.append(all_modes[i][orbital])
                orbital += 1
            atoms[j].set_eigenvector(mode_i)
            atoms[j].set_total_orbitals(len(all_modes))
            atoms[j].set_quantum_dict(quantum_dict.get(atoms[j].get_symbol(), None))
            atoms[j].set_eigenenergies(energies)


def input_file_setup(out_file, attributes_file, wf_file):  # Initialises atoms using .out, attributes.txt and .wf
    orb_dict, quantum_dict = create_orbital_dict(out_file)
    atoms = create_all_atoms(out_file)
    set_attr_from_file(attributes_file, atoms)
    all_modes, energies = eig_arr_from_wf(wf_file, atoms, orb_dict)
    set_eig_to_atoms(atoms, orb_dict, quantum_dict, all_modes, energies)
    return atoms


def xyz_to_plato_input(xyz_file, input_file="config/default.in"):
    basename = ntpath.basename(xyz_file)
    name = os.path.splitext(basename)[0]

    try:
        with open(input_file, "r") as f:
            contents = f.readlines()
    except IOError:
        raise FileNotFoundError

    try:
        with open(xyz_file, "r") as xyz:
            natoms = xyz.readline().strip()
            xyz.readline()
            xyz_contents = xyz.readlines()
    except IOError:
        raise IOError

    contents.insert(get_line_number(input_file, "NAtom"), natoms)
    line_number = get_line_number(input_file, "Atoms") + 1
    for line, content in enumerate(xyz_contents):
        contents.insert(line + line_number, content)

    now = datetime.now()
    date = now.strftime("%d-%m_%H%M%S")
    with open(name + "_" + date + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return name + "_" + date


def trans_plato_input(xyz_file, selected, input_file="config/default_trans.in"):
    basename = ntpath.basename(xyz_file)
    name = os.path.splitext(basename)[0]

    if len(selected) <= 1:
        raise AssertionError

    try:
        with open(input_file, "r") as f:
            contents = f.readlines()
    except IOError:
        raise FileNotFoundError

    try:
        with open(xyz_file, "r") as xyz:
            natoms = xyz.readline().strip()
            xyz.readline()
            xyz_contents = xyz.readlines()
    except IOError:
        raise IOError

    terminal_line_count = get_line_number(input_file, "OpenBoundaryTerminals")
    contents.insert(terminal_line_count, str(len(selected)) + " 1 -100.0 -0.4281406\n")
    for i in range(len(selected)):
        contents.insert(terminal_line_count + i + 1, "0.0 0.10 0.001 0 1 " + str(selected[i]) + "\n")

    contents.insert(get_line_number(input_file, "NAtom") + i + 2, natoms)
    line_number = get_line_number(input_file, "Atoms") + i + 3
    for line, content in enumerate(xyz_contents):
        contents.insert(line + line_number, content)

    now = datetime.now()
    date = now.strftime("%d-%m_%H%M%S")
    with open(name + "_t_" + date + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return name + "_t_" + date


def curr_plato_input(xyz_file, selected, regionA, regionB, reference_pot, bias, gamma, current_calc,
                     input_file="config/default_curr.in"):
    basename = ntpath.basename(xyz_file)
    name = os.path.splitext(basename)[0]

    if len(selected) <= 1:
        raise AssertionError

    if len(regionA) <= 0:
        raise ValueError

    if len(regionB) <= 0:
        raise ZeroDivisionError

    try:
        with open(input_file, "r") as f:
            contents = f.readlines()
    except IOError:
        raise FileNotFoundError

    try:
        with open(xyz_file, "r") as xyz:
            natoms = xyz.readline().strip()
            xyz.readline()
            xyz_contents = xyz.readlines()
    except IOError:
        raise IOError

    terminal_line_count = get_line_number(input_file, "OpenBoundaryTerminals")
    contents.insert(terminal_line_count, str(len(selected)) + " 1 -100.0 " + str(reference_pot) + "\n")
    for i in range(len(selected)):
        if current_calc:
            if i == 0:
                contents.insert(terminal_line_count + i + 1,
                                str(bias * 0.5 / RYDBERG) + " " + str(gamma) + " 0.001 0 1 " + str(selected[i]) + "\n")
            if i == 1:
                contents.insert(terminal_line_count + i + 1,
                                str(bias * -0.5 / RYDBERG) + " " + str(gamma) + " 0.001 0 1 " + str(selected[i]) + "\n")
        else:
            contents.insert(terminal_line_count + i + 1,
                            str(bias / RYDBERG) + " " + str(gamma) + " 0.001 0 1 " + str(selected[i]) + "\n")

    contents.insert(get_line_number(input_file, "NAtom") + i + 2, natoms)
    line_number = get_line_number(input_file, "Atoms") + i + 3
    for line, content in enumerate(xyz_contents):
        contents.insert(line + line_number, content)

    current_line_count = get_line_number(input_file, "OpenBoundaryCurrent") + 1
    region_A = str(len(regionA)) + " " + " ".join(map(str, regionA)) + "\n"
    region_B = str(len(regionB)) + " " + " ".join(map(str, regionB)) + "\n"
    contents.insert(current_line_count + i + 2, region_A)
    contents.insert(current_line_count + i + 3, region_B)

    now = datetime.now()
    date = now.strftime("%d-%m_%H%M%S")
    with open(name + "_c_" + date + "_" + str(bias) + "V_G-" + str(gamma) + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return name + "_c_" + date + "_" + str(bias) + "V_G-" + str(gamma)


def find_current_in_file(file):
    with open(file, "r") as f:
        string = lines_that_contain("Current[0]", f)[0]
    return string[13:-4]


def isfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    if float(string) == float("inf") or float(string) == float("-inf") or math.isnan(float(string)):
        return False
    return True


def isposfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    if float(string) == float("inf") or float(string) == float("-inf") or math.isnan(float(string)):
        return False
    if float(string) < 0:
        return False
    return True


def isdigit(string):
    if not string.isdigit():
        return False
    if string.strip() == "0":
        return False
    return True


if __name__ == '__main__':
    pass

    # atoms_main = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")
    # xyz_to_plato_input("benzene.xyz")

    # for i in range(12):
    # atoms_main[i].check()
    # print('\n')

    # xyz_to_plato_input("benzene.xyz")
