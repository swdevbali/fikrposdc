from main import app, db, login_manager
from flask import render_template, request, flash, url_for, redirect, abort, jsonify, session, g
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_user, logout_user, current_user, login_required, UserMixin
import models, json,  os, string, forms, helper


@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('DashboardView:index'))
    return render_template('index.html', login_form = forms.LoginForm())

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(userid):
    return models.Users.query.get(userid)

class DashboardView(FlaskView):
    route_base='/dashboard'
    
    def index(self):
        return render_template('dashboard.html')


class SignView(FlaskView):
    route_base = '/auth'

    @route('/signin', methods=['POST'])
    def signin(self):
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('DashboardView:index'))

        form = forms.LoginForm(request.form)
        if form.validate():
            user = models.Users.query.filter_by(username = form.username.data).first()

            if user is None:
                return redirect(url_for('SignView:dedicated'))            
            if user.password != helper.hash_pass(form.password.data):
                return redirect(url_for('SignView:dedicated'))                

            login_user(user, remember = form.remember_me.data)            
            
            session['logged'] = True
            session['username']= user.username
            session['company_id'] = user.company_id
            return redirect(url_for('index'))        
        return redirect(url_for('SignView:dedicated'))    

    def signout(self):
        session.pop('logged')
        session.pop('username')
        session.pop('company_id')
        logout_user()
        return redirect(url_for('index'))

    def dedicated(self):
        return render_template('/login.html', login_form = forms.LoginForm())

class RegistrationView(FlaskView):
    route_base='/registration'
    def signup(self):
        return render_template('signup.html', 
                               form = forms.RegistrationForm(),
                               login_form = forms.LoginForm())

    def post(self):
        form = forms.RegistrationForm(request.form)
        if form.validate():
            user = models.Users()
            form.populate_obj(user)
            
            user_exist = models.Users.query.filter_by(username=form.username.data).first()
            email_exist = models.Users.query.filter_by(email=form.email.data).first()

            if user_exist:
                form.errors['username']=[]
                form.errors['username'].append('Username already taken')

            if email_exist:
                form.errors['email']=[]
                form.errors['email'].append('Email already use')

            if user_exist or email_exist:
                return render_template('signup.html', 
                                       form = form,
                                       login_form = forms.LoginForm())
            

            user.password = helper.hash_pass(user.password)
            company = models.Companies()
            company.name = form.company_name.data
            company.users.append(user)
            db.session.add(company)
            db.session.commit()

            return redirect(url_for('RegistrationView:success'))
            
        return render_template('signup.html', 
                               form = form,
                               login_form = forms.LoginForm())

           
    def success(self):
        return render_template('signup_success.html',
                                   login_form = forms.LoginForm())
class DashBoard(FlaskView):
    route_base = '/dashboard'
    
    @login_required
    def index(self):
        return render_template('dashboard.html')

class UserView(FlaskView):
    route_base = '/dashboard/manage/users'
    
    @login_required
    def index(self):
        return render_template('users/list.html')

    @login_required    
    def new(self):
        form = forms.UserForm()
        return render_template('users/form.html', form=form)
   
    @login_required
    def post(self):
        form = forms.UserForm(request.form)
        if form.validate():
            if form.id.data=='':
                user = models.Users()
                form.populate_obj(user)
                user.id = None
                company = models.Companies.query.get(session['company_id'])
                company.users.append(user)
            else:
                user = models.Users.query.get(form.id.data)
                form.populate_obj(user)
            
            db.session.commit()            
            return redirect(url_for('UserView:index'))
        return render_template('users/form.html', form=form)

    @login_required
    def view(self,user_id):
        user = models.Users.query.get(user_id)
        form = forms.UserForm(obj=user)
        return render_template('users/form.html', form=form)

    @login_required
    def delete(self, user_id):
        user = models.Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('UserView:index')) #not used

    @login_required
    def apidelete(self, user_id):
        user = models.Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit() #todo result
        result = {}
        result['result']='success'
        return json.dumps(result)

class BranchView(FlaskView):
    route_base = '/dashboard/manage/branches'

    @login_required
    def index(self):
        return render_template('branches/list.html')

    @login_required
    def new(self):
        form = forms.BranchForm()
        return render_template('branches/form.html', form=form)

    @login_required
    def post(self):
        form = forms.BranchForm(request.form)
        if form.validate():
            company = models.Companies.query.get(session['company_id'])
            if form.id.data=='':
                branch = models.Branches()
                form.populate_obj(branch)
                branch.id = None
                company.branches.append(branch)
            else:
                branch = models.Branches.query.get(form.id.data)
                form.populate_obj(branch)
            
            db.session.commit()   
            return redirect(url_for('BranchView:index'))
        return render_template('branches/form.html', form=form)

    @login_required
    def view(self,branch_id):
        branch = models.Branches.query.get(branch_id)
        form = forms.BranchForm(obj=branch)
        return render_template('branches/form.html', form=form)
    
    @login_required
    def apidelete(self, branch_id):
        branch = models.Branches.query.get(branch_id)
        db.session.delete(branch)
        db.session.commit() #todo result
        result = {}
        result['result']='succes/s'
        return json.dumps(result)

class DataSet(FlaskView):
    route_base = '/dataset'

    @login_required
    @route('/users/<int:company_id>')
    def users(self, company_id):
        data = {}
        data['iTotalRecords'] = 2
        data['sEcho'] = 1
        data['iTotalDisplayRecords'] =  2
        
        aaData = []   
        users=models.Users.query.with_entities(
            models.Users.id, models.Users.username,
            models.Users.email).filter_by(company_id=company_id).order_by(models.Users.username).all()
        for user in users:
            aaData.append([user.username, user.email, string.join(['<a href="',url_for('UserView:view', user_id=user.id),'"><i class="icon-pencil"></i></a> <a id="remove_user_',`user.id`,'" href="#"><i class="icon-remove"></i></a>'],'')])
    
        data['aaData']=aaData
        return json.dumps(data)
        
    @route('/branches/<int:company_id>')
    @login_required
    def branches(self, company_id = None):
        data = {}
        data['iTotalRecords'] = 2
        data['sEcho'] = 1
        data['iTotalDisplayRecords'] =  2    
        
        aaData = []   
        company = models.Companies.query.get(company_id)
        for branch in company.branches:
            aaData.append([branch.name, branch.address, branch.token, string.join(['<a href="',url_for('BranchView:view',branch_id=branch.id),'"><i class="icon-pencil"></i></a> <a id="remove_branch_',`branch.id`,'" href="#"><i class="icon-remove"></i></a>'])])
    
        data['aaData']=aaData
        return json.dumps(data)

    @route('/daily_cash_flow/<int:company_id>')
    @login_required
    def dailyCashFlow(self, company_id):
        '''bringing report dailycashflow'''
        data  = []
        datum = {}

        company = models.Companies.query.get(company_id)
        q = db.session.query(models.DailyCashFlow, models.Branches).with_entities(models.DailyCashFlow.day, models.Branches.name, models.DailyCashFlow.income).\
            join(models.Branches).\
            filter_by(company_id = company_id).\
            order_by(models.DailyCashFlow.day)
        
        data  = []
        datum = {}
        prev_day = None
        
        for row in q.all():
            if prev_day != row.day:
                datum = {}
                datum['hari']= helper.dump_date(row.day)
                datum[row.name] = row.income
                prev_day = row.day
            else:
                datum[row.name] = row.income
                data.append(datum)
                prev_day = row.day
            
        return json.dumps(data)

    @route('/branches_names/<int:company_id>')
    @login_required
    def branches_names(self, company_id):
        data = []
        company = models.Companies.query.get(company_id)
        branches = company.branches.with_entities(models.Branches.name).all()
        for branch in branches:
            data.append(branch.name)
        return json.dumps(data)

class CompanyView(FlaskView):
    route_base = '/dashboard/manage/company'

    @login_required
    @route('/profile', methods=['GET', 'POST'])
    def profile(self):
        if request.method=='POST':
            company = models.Companies.query.get(request.form['id'])
            company.name = request.form['name']
            company.address = request.form['address']
            company.token = request.form['token']
            db.session.commit()
            flash('success')
            return redirect(url_for('CompanyView:profile'))
        return render_template('companies/form.html', 
                               company=models.Companies.query.get(session['company_id']))




DashBoard.register(app)
UserView.register(app)
BranchView.register(app)
DataSet.register(app)
RegistrationView.register(app)
SignView.register(app)
CompanyView.register(app)
DashboardView.register(app)
