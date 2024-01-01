"""Blogly application."""

from flask import Flask, request, redirect, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
# from flask_migrate import Migrate

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'anotherone'

connect_db(app)
db.create_all()
# migrate = Migrate(app, db)


@app.route('/')
def go_to_users_page():
    """go to users' page"""
    users = User.query.all()
    return render_template('users.html', users=users)

# @app.route('/add_user')
# def add_user():
#     """go to add_user form page"""
#     return render_template('add_user.html')

@app.route('/add_user_page')
def go_to_add_user_page():
    return render_template("add_user.html")


@app.route('/submit_form', methods=['POST'])
def create_single_user_from_info():
    """receive and process data from form"""
    new_user = User(
        first_name = request.form['first'],
        last_name = request.form['last'],
        picture = request.form['picture']
    )
    db.session.add(new_user)
    db.session.commit()
#create list of User objects
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/single_user_page/<int:id>')
def create_single_user(id):
    """get user's information and put on own page"""
#return user object
    user=User.query.get(id)
    # post=Post.query.get(id)  
    ##################don't need Post.query since have posts = db.relationship("Post", backref="user", cascade="all, delete-orphan") 
    return render_template('single_user.html', user=user)   
    # return render_template('single_user.html', first=first, last=last, picture=img, iid=iid)


@app.route('/single_user_edit/<int:id>')
def edit_single_user(id):
    """put the user's information on own page so can edit"""
    user = User.query.get(id)
    return render_template('edit_user.html', user=user)


@app.route('/submit_edit_form/<int:id>', methods=['POST'])
def edit_user_info(id):
    """receive and process data from form for editing user info"""
    user = User.query.get(id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.picture = request.form['picture'] 
    db.session.add(user)
    db.session.commit()
    return redirect(f'/single_user_page/{id}')


@app.route('/single_user_delete/<int:id>')
def delete_user(id):
    user = User.query.get(id)
################
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

#############################################POSTS################################
#i think this should be the id of the post
@app.route('/individual_post/<int:id>')
def show_individual_post(id):
    """show user's individual post using post id"""
    post = Post.query.get(id)
    return render_template('see_post.html', post=post)


@app.route('/post_form/<int:id>')
def post_form(id):
    """go to blog_post_form.html and create post"""
    user = User.query.get(id)
    tags = Tag.query.all()
    return render_template('blog_post_form.html', user=user, tags=tags)


@app.route('/post_add/<int:id>', methods=['POST'])
def add_post(id):
    '''add post to database and return to to single user page'''
    user = User.query.get(id)
    # user_id=user.id
    # title = request.form['title']
    # post = request.form['post']
    # postee = Post()
    # postee.title = title
    # postee.post = post
    # postee.user_id = user.id

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    post=request.form['post'],
                    user=user,
                    tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    return redirect (f'/single_user_page/{user.id}')

#endpoint for when user wants to edit own post
@app.route('/edit_post/<int:id>')
def edit_post(id):
    """get individual post row from database and display on edit_post.html"""
    post = Post.query.get(id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/delete_post/<int:id>')
def delete_post(id):
    post = Post.query.get(id)
################
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/edited_post/<int:id>', methods=['POST'])
def edited_post(id):
    """update post in database and return to single user page"""
    # update database by updating attributes for the post
    post = Post.query.get(id)
    post.title = request.form['title']
    post.post = request.form['post']
   
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.add(post)
    db.session.commit()
    return redirect(f'/individual_post/{id}')


###################################TAGS#####################################################
@app.route("/tags")
def display_tags():     
    """show all of the tags"""
    all_tags = Tag.query.all()
    return render_template("tags/all_tags.html", all_tags=all_tags)


@app.route("/tag_page/<int:id>")
def show_individual_tag(id):
    tag = Tag.query.get(id)
    return render_template("tags/show_tag.html", tag=tag)


@app.route("/add_tag")
def add_a_new_tag():
    # return render_template('tags/create_tag.html', user=user)
    return render_template('tags/create_tag.html')
    # return render_template('tags/create_tag.html')


@app.route("/submit_new_tag", methods=['POST'])
def get_info_from_new_tag_form():
    tag = Tag()
    tag_name = request.form['tagname']
    tag.name = tag_name
    db.session.add(tag)
    db.session.commit()

    ##################don't need Post.query since have posts = db.relationship("Post", backref="user", cascade="all, delete-orphan") 
    return redirect('/')


@app.route("/all_tags")
def see_all_tags():
    tags = Tag.query.all()
    return render_template('tags/all_tags.html', tags=tags)


@app.route("/edit_tag/<int:id>")
def edit_a_tag(id):
    tag = Tag.query.get(id)
    return render_template("tags/edit_tag.html", tag=tag)


@app.route("/delete_tag/<int:id>")
def delete_tag_from_database(id):
    tag = Tag.query.get(id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/")




















    


