import unittest
from main import db
import models
import md5
import helper

class DbTest(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        
    def test_user_and_company(self):
        """admin of a company"""
        
        user1 = models.Users('eko', helper.hash_pass('rahasia'), 'swdev.bali@gmail.com')
        db.session.add(user1)
        db.session.commit()
        
        """the company"""
        company1 = models.Companies('CDI','Glagah Kidul', 'empty')
        db.session.add(company1)
        company1.users.append(user1)
        db.session.commit()        
        assert company1.users[0].id == user1.id

        """branches"""
        company1.branches.append(models.Branches(name='Kopjar',address='Penjara Malaysia', token='empty token', user_id=user1.id))
        company1.branches.append(models.Branches(name='Selangor',address='Koperasi Selangor', token='empty token',  user_id=user1.id))        
        db.session.commit()
        
        #assert branch1.company_id == branch2.company_id;


if __name__ == '__main__':
    
    unittest.main()
