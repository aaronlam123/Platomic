import numpy as np


class Atom:
    def __init__(self, symbol, x, y, z, index, radius=None):
        self.__symbol = symbol
        self.__x = x
        self.__y = y
        self.__z = z
        self.__index = index
        self.__colour = None
        self.__radius = radius
        self.__bonding = None
        self.__eigenvector = None
        self.__total_orbitals = None
        self.__quantum_dict = None
        self.__eigenenergies = None
        self.__isSelectedTrans = 0
        self.__isSelectedCurrA = False
        self.__isSelectedCurrB = False
        self.__mi = None
        self.__maxBonds = None
        self.__bondCount = None
        self.__skipOrbital = None

    # Getter functions
    def get_symbol(self):
        return self.__symbol

    def get_xyz(self):
        return [float(self.__x), float(self.__y), float(self.__z)]

    def get_radius(self):
        return float(self.__radius)

    def get_bonding(self):
        return self.__bonding

    def get_colour(self):
        return self.__colour

    def get_eigenvector(self, mode):
        return np.array(self.__eigenvector[mode]).astype(float)

    def get_total_orbitals(self):
        return self.__total_orbitals

    def get_quantum_dict(self):
        return self.__quantum_dict

    def get_eigenenergies(self):
        return self.__eigenenergies

    def get_eigenenergy(self, mode):
        return self.__eigenenergies[mode]

    def get_isSelectedTrans(self):
        return self.__isSelectedTrans

    def get_isSelectedCurrA(self):
        return self.__isSelectedCurrA

    def get_isSelectedCurrB(self):
        return self.__isSelectedCurrB

    def get_mi(self):
        return self.__mi

    def get_index(self):
        return self.__index

    def get_maxBonds(self):
        return self.__maxBonds

    def get_bondCount(self):
        return self.__bondCount

    def get_skipOrbital(self):
        return self.__skipOrbital

    # Setter functions
    def set_colour(self, colour):
        self.__colour = colour

    def set_radius(self, radius):
        self.__radius = radius

    def set_bonding(self, element):
        if self.__bonding is None:
            self.__bonding = [element]
        self.__bonding.append(element) if element not in self.__bonding else self.__bonding

    def set_eigenvector(self, eigenvector):
        if self.__eigenvector is None:
            self.__eigenvector = [eigenvector]
            return
        self.__eigenvector.append(eigenvector)

    def set_total_orbitals(self, number):
        self.__total_orbitals = number

    def set_quantum_dict(self, quantum_dict):
        self.__quantum_dict = quantum_dict

    def set_eigenenergies(self, eigenenergies):
        self.__eigenenergies = eigenenergies

    def set_isSelectedTrans(self, terminal):
        self.__isSelectedTrans = terminal

    def set_isSelectedCurrA(self, state):
        self.__isSelectedCurrA = state

    def set_isSelectedCurrB(self, state):
        self.__isSelectedCurrB = state

    def set_mi(self, mi):
        self.__mi = mi

    def set_maxBonds(self, count):
        self.__maxBonds = int(count)
        self.__bondCount = int(count)

    def set_skipOrbital(self, boolean):
        self.__skipOrbital = boolean

    def reset_bonds(self):
        self.__bondCount = self.__maxBonds

    def decrement_bond_count(self):
        self.__bondCount -= 1
