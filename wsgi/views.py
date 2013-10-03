from main import app, db
from flask import render_template, request, flash, url_for, redirect, abort, jsonify
from flask.ext.classy import FlaskView
import models, json,  os, string, forms

class GeneralView(FlaskView):
    route_base = '/'
    def index(self):
        return render_template('index.html')

class UserView(FlaskView):
    route_base = '/manage/users'

    def index(self):
        return render_template('users/list.html')
    
    def new(self):
        form = forms.UserForm()
        return render_template('users/form.html', form=form)
   
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

    def view(self,user_id):
        user = models.Users.query.get(user_id)
        form = forms.UserForm()
        form.id.data = user.id
        form.email.data = user.email
        form.username.data = user.username
        form.password.data = user.password
        form.password_confirm.data = user.password
        return render_template('users/form.html', form=form)

    def delete(self, user_id):
        user = models.Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('UserView:index')) #not used

    def apidelete(self, user_id):
        user = models.Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit() #todo result
        result = {}
        result['result']='success'
        return json.dumps(result)

class BranchView(FlaskView):
    route_base = '/manage/branches'

    def index(self):
        return render_template('branches/list.html')

    def new(self):
        return render_template('branches/form.html', branch=None)

    def post(self):
        if request.form['id']=='':
            company = models.Companies.query.get(1)
            branch = models.Branches(request.form['name'], request.form['address'], request.form['token'],None)
            company.branches.append(branch)
        else:
            branch = models.Branches.query.get(request.form['id'])
            branch.name = request.form['name']
            branch.address = request.form['address']
            branch.token = request.form['token']

        db.session.commit()
        return redirect(url_for('BranchView:index'))

    def view(self,branch_id):
        branch = models.Branches.query.get(branch_id)
        return render_template('branches/form.html', branch=branch)

    def apidelete(self, branch_id):
        branch = models.Branches.query.get(branch_id)
        db.session.delete(branch)
        db.session.commit() #todo result
        result = {}
        result['result']='succes/s'
        return json.dumps(result)

class DataSet(FlaskView):
    route_base = '/dataset'

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
        
    def branches(self):
        data = {}
        data['iTotalRecords'] = 2
        data['sEcho'] = 1
        data['iTotalDisplayRecords'] =  2    
        
        aaData = []   
        company = models.Companies.query.get(1)    
        for branch in company.branches:
            aaData.append([branch.name, branch.address, string.join(['<a href="',url_for('BranchView:view',branch_id=branch.id),'"><i class="icon-pencil"></i></a> <a id="remove_branch_',`branch.id`,'" href="#"><i class="icon-remove"></i></a>'])])
    
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


GeneralView.register(app)
UserView.register(app)
BranchView.register(app)
DataSet.register(app)
