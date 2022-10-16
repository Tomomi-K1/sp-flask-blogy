"""Blogly application."""


from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
toolbar = DebugToolbarExtension(app)

# using function created in model connect_db 
connect_db(app)
# create database from model py
db.create_all()

# ================User route=======================
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

    # springboard solution=======
    # you can just assign the value directly to user.first_name so that you don't need to do "first_name = request.form['first_name']"
    # user = User.query.get_or_404(user_id)
    # user.first_name = request.form['first_name']
    # user.last_name = request.form['last_name']
    # user.image_url = request.form['image_url']

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
    tags = Tag.query.all()
    return render_template('post-form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')
    
    new_post = Post(title=title, content=content, user_id=user_id )
    for tag in tags:
        tag_id = Tag.query.get(tag)
        new_post.tags.append(tag_id)
    db.session.add(new_post)
    db.session.commit()

    # springboard solution==========
    # user = User.query.get_or_404(user_id)
    # tag_ids = [int(num) for num in request.form.getlist("tags")] 
    # ==above creates the list of tag ids in checked tags===
    # tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # ===this is same as "SELECT * FROM tags table WHERE tag.id IN tags_ids"=====
    # ====.in_(aaa), aaa could be list when you use with filter, you can just select the tags that tag_ids.
    # new_post = Post(title=request.form['title'],
    #                 content=request.form['content'],
    #                 user=user,
    #                 tags=tags)

    # ????===== user = user, tags= tags are created from relationship???

    # db.session.add(new_post)
    # db.session.commit()


    return redirect(url_for('show_user_detail', user_id=user_id))

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show a post.Show buttons to edit and delete the post."""
    
    post =Post.query.get(post_id)
    tags =post.tags
    
    return render_template('post-detail.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit_form(post_id):
    """Show a form to edit an existing post"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    checked_tag = post.tags
    return render_template('post-edit-form.html', post=post, tags=tags,checked_tag=checked_tag)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_editted_post(post_id):
    """Handle form submission for updating an existing post"""
   
    tags = request.form.getlist('tags')

    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    for tag in post.tags:
        if tag.id not in tags:
            tag=Tag.query.get(tag.id)
            post.tags.remove(tag)
    
    for tag in tags:
        tag_id = Tag.query.get(tag)
        post.tags.append(tag_id)

# ====springboard solution=========#
# @app.route('/posts/<int:post_id>/edit', methods=["POST"])
# def posts_update(post_id):
#     """Handle form submission for updating an existing post"""

#     post = Post.query.get_or_404(post_id)
#     post.title = request.form['title']
#     post.content = request.form['content']

#     tag_ids = [int(num) for num in request.form.getlist("tags")]
#     post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # this is better way than how I did since if post.tags brought up 3 tags, but now user changed only 2 tags are related to the post, by using "post.tags" will update the 3 tags to 2 tags so you don't need to separately remove or 

#     db.session.add(post)
#     db.session.commit()

#     db.session.add(post)
#     db.session.commit()


    return redirect(url_for('show_post_details', post_id =post_id))
    # or you could write return redirect(f"/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """delete a user and redirect to the list of users"""

    post =Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('show_user_detail', user_id=post.user_id))
     # or you could write return redirect(f"/users/{post.user_id}')


# ======================== Tag route============================
@app.route('/tags')
def show_all_tags():
    """list up all tags"""
    tags = Tag.query.all()

    return render_template('tag-list.html', tags=tags)
    
@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """show tag's name and posts that has the tag"""

    tag = Tag.query.get(tag_id)
    
    return render_template('tag-detail.html', tag=tag)

@app.route('/tags/new', methods=["GET"])
def show_tag_form():
    """Shows a form to add a new tag."""
    return render_template('tag-form.html')

@app.route('/tags/new', methods=["POST"])
def handle_add_tag():
    """Process add form, adds tag, and redirect to tag list."""
    tag = Tag(name=request.form['tag-name'])

    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def edit_tag(tag_id):
    """Show edit form for a tag."""
    tag=Tag.query.get(tag_id)
    return render_template('tag-edit-form.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    tag=Tag.query.get(tag_id)
    tag.name=request.form['tag-name']

    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """delete a tag"""
    tag = Tag.query.get(tag_id)
    
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')




