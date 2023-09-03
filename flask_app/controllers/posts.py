from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User

#CREATE controllers
@app.route('/new/sighting') #GET route to render form
def new_post():
    return render_template('add_new.html')


@app.route('/new/sighting', methods=['POST'])
def create_post():
    # check to see if anyone is in session, if not, redirect to the login page, if they are, then open a new code block.
    if 'user_id' not in session:
        return redirect ('/')
        # if validate recipe 
    if Post.validate_post(request.form):
        # Create data dictionary to catch the request.form input fields
        data = {
            "location": request.form['location'],
            "message": request.form['message'],
            "quantity": int(request.form['quantity']),
            "sighting_date": request.form['sighting_date'],
            "users_id": session['user_id'],
            "first_name": session['first_name']
        }
        # (if user in session) Create an id variable for the session user
        Post.save(data)
        # Call the insert method 
        return redirect('/users/dashboard')
    return redirect ('/new/sighting') 



#READ controllers
@app.route('/post/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'post_id' : id
    }
    print(Post.show_by_id(data))
    return render_template('show_post.html', post=Post.show_by_id(data))




#UPDATE controllers
@app.route('/edit/post/<int:id>') #GET route to render form
def render_edit(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'post_id' : id
    }
    return render_template('edit.html', post=Post.show_by_id(data))


@app.route('/edit/post/<int:id>', methods = ['POST'])
def edit_post(id):
    if 'user_id' not in session:
        return redirect ('/')
    if Post.validate_post(request.form):
    # Create data dictionary to catch the request.form input fields
        data = {
            "location": request.form['location'],
            "message": request.form['message'],
            "quantity": int(request.form['quantity']),
            "sighting_date": request.form['sighting_date'],
            "users_id": session['user_id'],
            "post_id": id
        }
        Post.edit_post(data)
        return redirect('/users/dashboard')
    return redirect (f'/edit/post/{id}')





#DELETE controllers
@app.route('/delete/post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'post_id' : id
    }
    Post.delete(data)
    return redirect ('/users/dashboard')

