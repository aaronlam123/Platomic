import ntpath
import pyqtgraph
from PyQt5 import QtGui
import shlex
from atom import Atom
import os


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
        new_entry = Atom(*xyz_split)
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
    total = total_orbitals(atoms, orb_dict)
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            if i % (total + 1) == 0:
                all_modes.append(a_mode)
                a_mode = []
                continue
            a_mode.append(line.strip())
    all_modes.append(a_mode)
    return all_modes


# sets 2D array of eigenvalues split by mode per atom, sets orbital count and quantum dict #
def set_eig_to_atoms(atoms, orb_dict, quantum_dict, all_modes):
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


def input_file_setup(out_file, attributes_file, wf_file):  # Initialises atoms using .out, attributes.txt and .wf
    orb_dict, quantum_dict = create_orbital_dict(out_file)
    atoms = create_all_atoms(out_file)
    set_attr_from_file(attributes_file, atoms)
    all_modes = eig_arr_from_wf(wf_file, atoms, orb_dict)
    set_eig_to_atoms(atoms, orb_dict, quantum_dict, all_modes)
    return atoms


def xyz_to_plato_input(xyz_file, input_file="config/default.in"):
    basename = ntpath.basename(xyz_file)
    name = os.path.splitext(basename)[0]

    with open(input_file, "r") as f:
        contents = f.readlines()

    try:
        with open(xyz_file, "r") as xyz:
            natoms = xyz.readline().strip()
            xyz.readline()
            xyz_contents = xyz.readlines()
    except IOError:
        raise

    contents.insert(243, natoms)
    for line, content in enumerate(xyz_contents):
        contents.insert(line + 250, content)

    with open(str(name) + "_.in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return name + "_"


if __name__ == '__main__':
    pass
    #atoms_main = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")

    #for i in range(12):
        #atoms_main[i].check()
        #print('\n')

    #xyz_to_plato_input("benzene.xyz")

