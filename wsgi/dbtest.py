import unittest
from main import db
import models

class DbTest(unittest.TestCase):
    def setUp(self):
        db.create_all()
        
    def test_company(self):
        assert 2==2

if __name__ == '__main__':
    unittest.main()
