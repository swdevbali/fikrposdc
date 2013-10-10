import unittest
from main import db
from sqlalchemy.exc import IntegrityError, DBAPIError, SQLAlchemyError
import models, md5,  helper, json


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")

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
        branch1 = company1.branches.filter(models.Branches.name=='Kopjar').first()
        assert branch1.name=='Kopjar' and branch1.company_id == company1.id
        
        '''first attempt on sales data'''
        day1 = models.DailyCashFlow(day='2013-01-01',cash_start_of_day = 0, cash_end_of_day = 500000)
        branch1.dailyCashFlow.append(day1)
        db.session.commit()
        assert day1.id is not None

        '''completing sale data'''
        branch2 = company1.branches.filter(models.Branches.name=='Selangor').first()
        assert branch2.name=='Selangor' and branch2.company_id == branch1.company_id
        
        day1 = models.DailyCashFlow(day='2013-01-01',cash_start_of_day = 300000, cash_end_of_day = 600000)
        branch2.dailyCashFlow.append(day1)
        db.session.commit()
        assert day1.id is not None

        '''2nd day'''
        day2 = models.DailyCashFlow(day='2013-01-02',cash_start_of_day = 0, cash_end_of_day = 400000)
        branch1.dailyCashFlow.append(day2)

        day2 = models.DailyCashFlow(day='2013-01-02',cash_start_of_day = 0, cash_end_of_day = 1000000)
        branch2.dailyCashFlow.append(day2)
        db.session.commit()
        assert day2.id is not None

        '''bringing report dailycashflow'''
        q = db.session.query(models.DailyCashFlow, models.Branches).with_entities(models.DailyCashFlow.day, models.Branches.name, models.DailyCashFlow.income).\
            join(models.Branches).\
            filter_by(company_id = company1.id).\
            order_by(models.DailyCashFlow.day)
        
        data  = []
        datum = {}
        prev_day = None
        '''TODO : Refine to be as method in helper class'''
        for row in q.all():
            if prev_day != row.day:
                datum = {}
                datum['hari']= dump_date(row.day)
                datum[row.name] = row.income
                prev_day = row.day
            else:
                datum[row.name] = row.income
                data.append(datum)
                prev_day = row.day
            
        print json.dumps(data)


        '''3rd day'''
        day3 = models.DailyCashFlow(day='2013-01-03',cash_start_of_day = 0, cash_end_of_day = 2000000)
        branch1.dailyCashFlow.append(day3)

        day3 = models.DailyCashFlow(day='2013-01-03',cash_start_of_day = 0, cash_end_of_day = 900000)
        branch2.dailyCashFlow.append(day3)
        db.session.commit()
        assert day3.id is not None

        '''test uniqueness'''
        day3_double = models.DailyCashFlow(day='2013-01-03',cash_start_of_day = 0, cash_end_of_day = 900000)
        branch2.dailyCashFlow.append(day3_double)

        #self.assertRaises(IntegrityError, db.session.commit)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        '''solve uniquness by testing first for existing report on dailycashflow for the branch, and update accordingly'''
        day3_double_solved = models.DailyCashFlow(day='2013-01-03',cash_start_of_day = 0, cash_end_of_day = 666000)
        check_day = models.DailyCashFlow.query.filter_by(branch_id = branch2.id, day = day3_double_solved.day).first()
        if check_day is not None:
            check_day.cash_start_of_day = day3_double_solved.cash_start_of_day 
            check_day.cash_end_of_day = day3_double_solved.cash_end_of_day
            check_day.calculateIncome()
            db.session.commit()
        else:
            branch2.dailyCashFlow.append(day3_double_solved) #will not get executed

        assert day3_double_solved.id is None

        assert check_day.cash_end_of_day == 666000


        
                

if __name__ == '__main__':    
    unittest.main()
