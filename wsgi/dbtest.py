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
        
        '''sales'''
        branch1 = company1.branches[0] # branch1 = company1.branches.filter().all() # via query
        assert branch1.company_id == company1.id

        branch1.sales.append(models.Sales(day='2013-02-02'))
        db.session.commit()
        sales = branch1.sales[0] # harus via query
        sales.data.append(models.SaleData(cash_start_of_day = 0, cash_end_of_day = 500000, income = 500000))
        db.session.commit()

if __name__ == '__main__':    
    unittest.main()
