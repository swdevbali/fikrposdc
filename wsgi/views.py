from main import app, db, login_manager
from flask import render_template, request, flash, url_for, redirect, abort, jsonify, session
from flask.ext.classy import FlaskView
from flask.ext.login import login_required
import models, json,  os, string, forms


@app.route('/')
def index():
    return render_template('index.html', login_form = forms.LoginForm())

@login_manager.user_loader
def load_user(userid):
    return models.Users.query.get(int(userid))

class SignView(FlaskView):
    route_base = '/auth'
    def signin(self):
        pass

    def signout(self):
        session.pop('logged')
        return redirect('/')

class RegistrationView(FlaskView):
    route_base='/registration'
    def signup(self):
        form = forms.RegistrationForm()
        return render_template('signup.html', form = form)

    def post(self):
        form = forms.RegistrationForm(request.form)
        if form.validate():
            user = models.Users()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            company = models.Companies()
            company.name = form.company_name.data
            company.user_id = user.id
            db.session.add(company)
            db.session.commit()
            
            session['logged']=True
            return render_template('signup_success.html')

        return render_template('signup.html', form = form)
            

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
                db.session.add(user)
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
            company = models.Companies.query.get(1)
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
    def users(self):
        data = {}
        data['iTotalRecords'] = 2
        data['sEcho'] = 1
        data['iTotalDisplayRecords'] =  2
        
        aaData = []   
        users=models.Users.query.with_entities(
            models.Users.id, models.Users.username,
            models.Users.email).order_by(models.Users.username).all()
        for user in users:
            aaData.append([user.username, user.email, string.join(['<a href="',url_for('UserView:view', user_id=user.id),'"><i class="icon-pencil"></i></a> <a id="remove_user_',`user.id`,'" href="#"><i class="icon-remove"></i></a>'],'')])
    
        data['aaData']=aaData
        return json.dumps(data)
        
    @login_required
    def branches(self):
        data = {}
        data['iTotalRecords'] = 2
        data['sEcho'] = 1
        data['iTotalDisplayRecords'] =  2    
        
        aaData = []   
        company = models.Companies.query.get(1)    
        for branch in company.branches:
            aaData.append([branch.name, branch.address, branch.token, string.join(['<a href="',url_for('BranchView:view',branch_id=branch.id),'"><i class="icon-pencil"></i></a> <a id="remove_branch_',`branch.id`,'" href="#"><i class="icon-remove"></i></a>'])])
    
        data['aaData']=aaData
        return json.dumps(data)

class CompanyView:
    @app.route('/manage/company', methods=['GET', 'POST'])
    def manage_company():
        if request.method=='POST':
            company = models.Companies.query.get(request.form['id'])
            company.name = request.form['name']
            company.address = request.form['address']
            company.token = request.form['token']
            db.session.commit()
            flash('success')
            return redirect(url_for('manage_company'))
        return render_template('companies/form.html', company=models.Companies.query.get(1)) #todo for active company

DashBoard.register(app)
UserView.register(app)
BranchView.register(app)
DataSet.register(app)
RegistrationView.register(app)
SignView.register(app)
