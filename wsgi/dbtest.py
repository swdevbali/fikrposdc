import unittest
from main import db
import models

class DbTest(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        
    def test_user_and_company(self):
        user1 = models.Users('eko', 'rahasia', 'swdev.bali@gmail.com')
        db.session.add(user1)
        db.session.commit()
        
        company1 = models.Companies('CDI','Glagah Kidul', user1.id, 'empty')
        db.session.add(company1)
        db.session.commit()        
        assert company1.user_id == user1.id

        

if __name__ == '__main__':
    unittest.main()
