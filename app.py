"""Blogly application."""


from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def redirect_to_user_list():
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """shows list of all users"""
    users = User.query.all()
    return render_template('users-list.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show user's detailed information"""  
    user = User.query.get_or_404(user_id) 
    return render_template('details.html', user=user)


@app.route('/users/new')
def new_user_form():
    return render_template('new-form.html')

@app.route('/users/new', methods=['POST'])
def post_new_user():
    """add a new user to users table"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form.get('url')

    new_user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')   



@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """show edit form"""    
    user=User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit(user_id):

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form.get('url')
    
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """delete a user and redirect to the list of users"""

    user =User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')



