import unittest
from input import *


class TestInput(unittest.TestCase):
    def test_lines_that_contain(self):
        with open("test_output.txt", "r") as self.f:
            self.assertEqual(lines_that_contain("symbol", self.f),
                             ['Chemical symbol           : C\n', 'Chemical symbol           : H\n'])

    def test_lines_that_start_with(self):
        with open("test_output.txt", "r") as self.f:
            self.assertEqual(lines_that_start_with("Atom", self.f), ['Atom Type #    1\n', 'Atom Type #    2\n'])

    def test_get_last_char(self):
        self.assertEqual(get_last_char("Chemical symbol           : H", "test_output.txt"), ["H"])

    def test_get_lines_between(self):
        self.assertEqual(get_lines_between("test_output.txt", "n l m     energy     occupancy    radius",
                                           "---------------------------", "----------------", False, True, 0),
                         ['2 0 0   -0.219760     2.000000     4.913288',
                          '2 1 0   0.272680     0.666670     4.913288',
                          '2 1 1   0.272680     0.666670     4.913288',
                          '2 1 2   0.272680     0.666660     4.913288'])
        self.assertEqual(get_lines_between("test_output.txt", "n l m     energy     occupancy    radius",
                                           "---------------------------", "----------------", False, True, 1),
                         ['1 0 0   -0.349079     1.000000     2.305467'])
        self.assertEqual(get_lines_between("test_output.txt", "Atomic positions (a0):", "Total forces (Ry/a0):"),
                         ['C       0.00000      2.65076      0.00000',
                          'H       0.00000      4.70597      0.00000',
                          'C      -2.29562      1.32538      0.00000',
                          'H      -4.07550      2.35299      0.00000',
                          'C      -2.29562     -1.32538      0.00000',
                          'H      -4.07550     -2.35299      0.00000',
                          'C       0.00000     -2.65076      0.00000',
                          'H       0.00000     -4.70597      0.00000',
                          'C       2.29562     -1.32538      0.00000',
                          'H       4.07550     -2.35299      0.00000',
                          'C       2.29562      1.32538      0.00000',
                          'H       4.07550      2.35299      0.00000'])
