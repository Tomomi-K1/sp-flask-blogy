"""Blogly application."""


from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_user_list():
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """shows list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users-list.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show user's detailed information"""  
    user = User.query.get_or_404(user_id) 
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template('details.html', user=user, posts=posts)


@app.route('/users/new')
def new_user_form():
    return render_template('new-form.html')

@app.route('/users/new', methods=['POST'])
def post_new_user():
    """add a new user to users table"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['url']
    url = url if url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=url)
    # springboard solution
    # new_user = User(
    #     first_name=request.form['first_name'],
    #     last_name=request.form['last_name'],
    #     image_url=request.form['image_url'] or None)
    
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')   

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """show edit form"""    
    user=User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit(user_id):

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['url']
    
    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    # user.image_url = url 
    user.image_url = url if url else "/static/default-pic.png" 

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """delete a user and redirect to the list of users"""

    user =User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# ======================== Posts route============================
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show form to add a post for that user"""
    user =User.query.get(user_id)

    return render_template('post-form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""

    title = request.form['title']
    content = request.form['content']
    
    new_post = Post(title=title, content=content, user_id=user_id )
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('show_user_detail', user_id=user_id))

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show a post.Show buttons to edit and delete the post."""
    
    post =Post.query.get(post_id)

    return render_template('post-detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit_form(post_id):
    """Show a form to edit an existing post"""
    post = Post.query.get(post_id)
    return render_template('post-edit-form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_editted_post(post_id):
    """Handle form submission for updating an existing post"""
    title = request.form['title']
    content = request.form['content']
    
    post = Post.query.get(post_id)
    post.title = title
    post.content = content 

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('show_post_details', post_id =post_id))
    # or you could write return redirect(f"/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """delete a user and redirect to the list of users"""

    post =Post.query.get(post_id)
    user_id=post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('show_user_detail', user_id=user_id))
     # or you could write return redirect(f"/users/{post.user_id}')







