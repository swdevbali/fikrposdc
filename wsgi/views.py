from main import app, db
from flask import render_template, request, flash, url_for, redirect, abort, jsonify
import models, json,  os, string

'''Helper'''
def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default).route('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manage/users')
def manage_users():
    return render_template('users/list.html', users=models.Users.query.order_by(models.Users.username).all())

@app.route('/manage/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method=='POST':
        user = models.Users(request.form['username'], request.form['email'], request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('manage_users'))
    return render_template('users/form.html', user=None)

@app.route('/manage/users/view/<int:user_id>', methods=['GET','POST'])
def show_or_update(user_id):
    user = models.Users.query.get(user_id)
    if request.method=='GET':
        return render_template('users/form.html', user=user)
    user.username = request.form['username']
    user.email = request.form['email']
    user.password = request.form['password']
    db.session.commit()
    return redirect(url_for('manage_users'))

@app.route('/manage/users/delete/<int:user_id>', methods=['GET','POST'])
def delete_user(user_id):
    user = models.Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_users'))

@app.route ('/dataset/users')
def dataset_users():
    data = {}
    data['iTotalRecords'] = 2
    data['sEcho'] = 1
    data['iTotalDisplayRecords'] =  2

    aaData = []   
    users=models.Users.query.with_entities(
        models.Users.id, models.Users.username,
        models.Users.email).order_by(models.Users.username).all()
    for user in users:
        aaData.append([string.join(['<a href="/manage/users/view/',`user.id`,'">', `user.id`, '</a>'],''), user.username, user.email, 'Modify'])
    
    data['aaData']=aaData
    return json.dumps(data)

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
