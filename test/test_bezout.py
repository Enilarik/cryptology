import unittest

from src.lib import bezout

class TestBezout(unittest.TestCase):

    def test_normal_case(self):
        a = 84
        b = 30
        gcd, x, y = bezout(a, b)
        self.assertEqual(x*a + y*b, gcd)

    def test_with_prime(self):
        a = 17
        b = 9
        gcd, x, y = bezout(a, b)
        self.assertEqual(x*a + y*b, 1)

    def test_with_prime_inverse(self):
        a = 9
        b = 17
        gcd, x, y = bezout(a, b)
        self.assertEqual(x*a + y*b, 1)

if __name__ == '__main__':
    unittest.main()
