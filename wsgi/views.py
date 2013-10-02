from main import app, db
from flask import render_template, request, flash, url_for, redirect, abort, jsonify
from flask.ext.classy import FlaskView
import models, json,  os, string

class GeneralView(FlaskView):
    route_base = '/'
    def index(self):
        return render_template('index.html')

class UserView(FlaskView):
    route_base = '/manage/users'

    def index(self):
        return render_template('users/list.html')
    
    def new(self):
        return render_template('users/form.html', user=None)
   
    def post(self):
        if request.form['id']=='':
            user = models.Users(request.form['username'], request.form['email'], request.form['password'])
            db.session.add(user)
        else:
            user = models.Users.query.get(request.form['id'])
            user.username = request.form['username']
            user.email = request.form['email']
            user.password = request.form['password']

        db.session.commit()
        return redirect(url_for('UserView:index'))

    def view(self,user_id):
        user = models.Users.query.get(user_id)
        return render_template('users/form.html', user=user)

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
            aaData.append([branch.name, branch.address, '<a href=""><i class="icon-pencil"></i></a> <a id="remove_user_',`branch.id`,'" href="#"><i class="icon-remove"></i></a>'])
    
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

    @app.route('/manage/branches/', methods=['GET', 'POST'])
    def manage_branches():
        return render_template('branches/list.html')


GeneralView.register(app)
UserView.register(app)
DataSet.register(app)
