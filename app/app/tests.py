# Sample tests

from re import S
from django.test import SimpleTestCase

from app import calc

class CalcTest(SimpleTestCase):
    """Test calc module"""

    def test_add(self):
        """Test Adding Numbers"""

        res = calc.add(5, 6)
    
        self.assertEqual(res, 11)
    
    def test_substract(self):
        """Test Subtracting Numbers"""

        res = calc.substract(5,6)

        self.assertEqual(res,-1)