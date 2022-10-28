import unittest
import math

from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def test_valid1(self):  # valid test case
        expression = "1 + 2"
        expected = 3
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid2(self):  # valid test case
        expression = "3 + 2 * 10"
        expected = 23
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid3(self):  # valid test case
        expression = "(3 + 2) * 10"
        expected = 50
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid4(self):  # valid test case
        expression = "(((((((((3) + (2))))) * (((10)))))))"
        expected = 50
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid5(self):  # valid test case
        expression = f"3 + 2 * 10 - sin({math.pi / 2})"
        expected = 22
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid6(self):  # valid test case
        expression = f"3 + 2 * 10 - sin(((((({math.pi / 2}))))))"
        expected = 22
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid7(self):  # valid test case
        expression = f"sin(sqrt(9) / 3 * {math.pi / 2})"
        expected = 1
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid8(self):  # valid test case
        expression = f"sin     (     sqrt(     9     ) / 3 * {math.pi / 2}     )"
        expected = 1
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid9(self):  # valid test case
        expression = f"3 + 4 * 4 * 4 / (1 - 3) ^ 2 ^ 3"
        expected = 4
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid10(self):  # valid test case
        expression = f"3 + 4 * 4 * 4 / (((1 - 3) ^ 2) ^ 3)"
        expected = 4
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid11(self):  # valid test case
        expression = f"3 + (4 * 4 * 4 / (1 - 5)) ^ 2"
        expected = 259
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid12(self):  # valid test case
        expression = f"3 + 4 * 4 / 1 - 5 ^ 2"
        expected = -6
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid13(self):  # valid test case
        expression = f"((2 * (6 / (9 + 3) * -10)) + 17) + 5.5 + sqrt(9) ^ 2"
        expected = 21.5
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid14(self):  # valid test case
        expression = f"-(2 + 6) / 2"
        expected = -4
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_valid15(self):  # invalid test case
        expression = f"(2 + 2 ^ -1)"
        expected = 2.5
        result = Calculator.calculate(expression)
        self.assertEqual(result, expected)

    def test_invalid1(self):  # invalid test case
        expression = f"1 / 0"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid2(self):  # invalid test case
        expression = f"1 + ((1 + 2)"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid3(self):  # invalid test case
        expression = f"((1 + 2) + 2"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid4(self):  # invalid test case
        expression = f"(blablablafunc(1) + 2))"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid5(self):  # invalid test case
        expression = f"2(2 + 2)"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid6(self):  # invalid test case
        expression = f"2(2 -+- 2)"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid7(self):  # invalid test case
        expression = f"+2(2 - 2)+"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid8(self):  # invalid test case
        expression = f"--2(2 - 2)"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)

    def test_invalid9(self):  # invalid test case
        expression = f"2(2 _ 2)"
        with self.assertRaises(Exception):
            Calculator.calculate(expression)
