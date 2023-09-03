from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

    #CREATE controllers

@app.route('/users/register', methods = ['POST'])
def register_user():
    user_id = user.User.create_user(request.form)
    if user_id :
        return redirect('/users/dashboard')
    else: 
        return redirect('/')

@app.route('/users/dashboard')
def user_dashboard():
    if 'user_id' in session:
        return render_template ('user_dashboard.html', posts=Post.get_all())
    else:
        return render_template('index.html')   

    #READ controllers


@app.route('/users/login', methods =['POST'])
def users_login():
    if user.User.login_user(request.form):
        return redirect('/users/dashboard')
    else: 
        return redirect('/')

    


    #UPDATE controllers




    #DELETE controllers

@app.route('/users/logout')
def logout_user():
    session.clear()
    return redirect('/')