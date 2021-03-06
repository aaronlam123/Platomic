import math
import ntpath
import pyqtgraph
from PyQt5 import QtGui
import pandas as pd
from atom import Atom
import os

RYDBERG = 13.605685


def lines_that_contain(string, f):
    return [line for line in f if string in line]


def lines_that_start_with(string, f):
    return [line for line in f if string in line.split()[:1]]


def get_last_two_chars(string, file):
    array = []
    with open(file, "r") as f:
        for line in lines_that_contain(string, f):
            array.append(line.strip()[-2:].strip())
    return array


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


def create_orbital_dict(file):
    orb_dict = {}
    quantum_dict = {}
    elements = get_last_two_chars("Chemical symbol           :", file)
    orbitals = get_last_two_chars("Number of orbitals        :", file)
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


def create_all_atoms(file):
    array = []
    xyz = get_lines_between(file, "Atomic positions (a0):", "Total forces (Ry/a0):")
    for i in range(len(xyz)):
        xyz_split = xyz[i].split()
        new_entry = Atom(*xyz_split, i + 1)
        array.append(new_entry)
    return array


def set_attr_from_file(file, atoms):
    for i in range(len(atoms)):
        with open(file, "r") as f:
            next(f)
            for line in lines_that_start_with(atoms[i].get_symbol(), f):
                attributes = line.split()
                atoms[i].set_colour(pyqtgraph.glColor(QtGui.QColor(attributes[1])))
                atoms[i].set_radius(attributes[2])
                atoms[i].set_maxBonds(attributes[3])
                atoms[i].set_skipOrbital(attributes[4])
                elem = 5
                while elem < (len(attributes)):
                    atoms[i].set_bonding(attributes[elem])
                    elem += 1


def total_orbitals(atoms, orb_dict):
    total = 0
    for i in range(len(atoms)):
        count = orb_dict.get(atoms[i].get_symbol(), None)
        total += int(count)
    return total


def eig_arr_from_wf(file, atoms, orb_dict):
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


def input_file_setup(out_file, attributes_file, wf_file):
    orb_dict, quantum_dict = create_orbital_dict(out_file)
    atoms = create_all_atoms(out_file)
    set_attr_from_file(attributes_file, atoms)
    all_modes, energies = eig_arr_from_wf(wf_file, atoms, orb_dict)
    set_eig_to_atoms(atoms, orb_dict, quantum_dict, all_modes, energies)
    return atoms


def xyz_to_plato_input(xyz_file, excess, session_id, input_file="config/default.in"):
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

    excess_line_count = get_line_number(input_file, "ElectronExcess")
    contents.insert(excess_line_count, str(excess))

    with open(session_id + "_" + name + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return session_id + "_" + name


def return_occupied_keys(selected):
    occupied_keys = 0
    for key in selected:
        if len(selected[key]) != 0:
            occupied_keys += 1
    return occupied_keys


def return_occupied_keys_list(selected):
    occupied_keys = []
    for key in selected:
        if len(selected[key]) != 0:
            occupied_keys.append(key)
    return occupied_keys


def trans_plato_input(xyz_file, selected, excess, gamma, step_size, session_id, input_file="config/default_trans.in"):
    basename = ntpath.basename(xyz_file)
    name = os.path.splitext(basename)[0]

    occupied_keys = return_occupied_keys(selected)

    if occupied_keys <= 1:
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

    actual_gamma = str(gamma)
    if gamma == 0:
        actual_gamma = str(0.000001)
    terminal_line_count = get_line_number(input_file, "OpenBoundaryTerminals")
    contents.insert(terminal_line_count, str(occupied_keys) + " 1 -100.0 0\n")
    for i, key in enumerate(selected):
        if len(selected[key]) == 0:
            continue
        contents.insert(terminal_line_count + i + 1,
                        "0.0 " + actual_gamma + " 0.001 0 " + str(len(selected[key])) + " " + ' '.join(
                            selected[key]) + "\n")
    i = occupied_keys - 1

    trans_line_count = get_line_number(input_file, "OpenBoundaryTransmission") + 1
    contents.insert(trans_line_count + i + 2, "-1.0 1.0 " + str(step_size) + "\n")

    contents.insert(get_line_number(input_file, "NAtom") + i + 3, natoms)
    line_number = get_line_number(input_file, "Atoms") + i + 4
    for line, content in enumerate(xyz_contents):
        contents.insert(line + line_number, content)

    excess_line_count = get_line_number(input_file, "ElectronExcess")
    contents.insert(excess_line_count, str(excess))

    with open(session_id + "_" + name + "_t_G_" + str(gamma) + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return session_id + "_" + name + "_t_G_" + str(gamma)


def curr_plato_input(xyz_file, selected, reg_a, reg_b, excess, reference_pot, bias, gamma, step_size, session_id,
                     input_file="config/default_curr.in"):
    basename = ntpath.basename(xyz_file)
    name = os.path.splitext(basename)[0]

    occupied_keys = return_occupied_keys(selected)

    if occupied_keys <= 1:
        raise AssertionError

    if occupied_keys != 2:
        raise NotImplementedError

    if len(reg_a) <= 0:
        raise ValueError

    if len(reg_b) <= 0:
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

    region_a = True
    terminal_line_count = get_line_number(input_file, "OpenBoundaryTerminals")
    contents.insert(terminal_line_count, str(occupied_keys) + " 1 -100.0 " + str(reference_pot) + "\n")
    for i, key in enumerate(selected):
        if len(selected[key]) == 0:
            continue
        if key in return_occupied_keys_list(selected):
            if region_a:
                contents.insert(terminal_line_count + i + 1,
                                str(bias * -0.5 / RYDBERG) + " " + str(gamma) + " 0.001 0 " + str(
                                    len(selected[key])) + " " + ' '.join(selected[key]) + "\n")
                region_a = False
            else:
                contents.insert(terminal_line_count + i + 1,
                                str(bias * 0.5 / RYDBERG) + " " + str(gamma) + " 0.001 0 " + str(
                                    len(selected[key])) + " " + ' '.join(selected[key]) + "\n")
        else:
            contents.insert(terminal_line_count + i + 1,
                            "0.0 0.10 0.001 0 " + str(len(selected[key])) + " " + ' '.join(selected[key]) + "\n")
    i = occupied_keys - 1

    trans_line_count = get_line_number(input_file, "OpenBoundaryTransmission") + 1
    contents.insert(trans_line_count + i + 2, "-1.0 1.0 " + str(step_size) + "\n")

    contents.insert(get_line_number(input_file, "NAtom") + i + 3, natoms)
    line_number = get_line_number(input_file, "Atoms") + i + 4
    for line, content in enumerate(xyz_contents):
        contents.insert(line + line_number, content)

    current_line_count = get_line_number(input_file, "OpenBoundaryCurrent") + 1
    reg_a_str = str(len(reg_a)) + " " + " ".join(map(str, reg_a)) + "\n"
    reg_b_str = str(len(reg_b)) + " " + " ".join(map(str, reg_b)) + "\n"
    contents.insert(current_line_count + i + 2, reg_a_str)
    contents.insert(current_line_count + i + 3, reg_b_str)

    excess_line_count = get_line_number(input_file, "ElectronExcess")
    contents.insert(excess_line_count, str(excess))

    with open(session_id + "_" + name + "_c_" + str(bias) + "V_G-" + str(gamma) + ".in", "w") as f:
        contents = "".join(contents)
        f.writelines(contents)

    return session_id + "_" + name + "_c_" + str(bias) + "V_G-" + str(gamma)


def find_current_in_file(file):
    with open(file, "r") as f:
        string = lines_that_contain("Current[0]", f)[0]
    return string[13:-4].strip()


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


def isnatnumber(string):
    if not string.isdigit():
        return False
    if string.strip() == "0":
        return False
    return True


def process_current_out(directory_name):
    files = os.listdir(directory_name)
    files.sort()
    bias_v = files[-1].split("_")[-2]
    bias = pyqtgraph.np.linspace(0, float(bias_v[:-1]), len(files))
    currents = []
    files_full = [os.path.join(directory_name, file) for file in
                  os.listdir(directory_name)]
    files_full.sort()
    for file in files_full:
        currents.append(float(find_current_in_file(file)))
    return bias_v, bias, currents


def transmission_headers(input_file, selected):
    headers = ['All']
    df = pd.read_csv(input_file, sep=",", quoting=3)
    headers.extend(list(df)[1:])
    if return_occupied_keys(selected) == 0:
        return headers, headers
    headers_mapped = headers
    index = 1
    for i, key in enumerate(selected):
        if key in return_occupied_keys_list(selected):
            headers_mapped = [ind.replace(" " + str(index), ",".join(selected[key])) for ind in headers_mapped]
            index += 1
    headers_mapped = [ind.replace(" -", " - ") for ind in headers_mapped]
    return headers_mapped, headers


def process_energy_gamma_trans_csv(directory_name, session_id):
    energy = None
    transmission = None
    if session_id is None:
        files = [file for file in os.listdir(directory_name) if file.endswith(".csv")]
    else:
        files = [file for file in os.listdir(directory_name) if file.endswith(".csv") and file.startswith(session_id)]
    files.sort()
    gamma_v = files[-1].split("_")[-2]
    gamma = pyqtgraph.np.linspace(0, float(gamma_v), len(files) + 1)
    files_full = [os.path.join(directory_name, file) for file in files]

    for file in files_full:
        ds = pd.read_csv(file, sep=',', header=0)
        if energy is None:
            energy = pyqtgraph.np.array(ds["E(Ry)"])
        if transmission is None:
            transmission = pyqtgraph.np.zeros((len(energy), 1))
        column = pyqtgraph.np.resize(pyqtgraph.np.array(ds[" 1 - 2"]), (len(energy), 1))
        transmission = pyqtgraph.np.append(transmission, column, axis=1)

    return energy, gamma, transmission


def find_chemical_potential(file):
    chemical_potentials = []
    lines = get_lines_between(file, "Terminal chemical potentials:", "Primitive translation vectors (a0):",
                              pop_twice=True)
    i = len(lines) - 1
    while lines[i] != "Terminal chemical potentials:":
        chemical_potentials.append(float(lines[i].split()[-1]))
        i -= 1
    in_rydberg = sum(chemical_potentials) / len(chemical_potentials)
    return in_rydberg * RYDBERG
