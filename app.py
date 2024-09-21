from flask import Flask, request, render_template, redirect, session, flash

from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Blog, Post, Tag, PostTag


from sqlalchemy import text


app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_user'

app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)


app.config['SECRET_KEY'] = "eh4j!j4cjfolks34jj5"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



#       ***     Uncomment to wipe table and add new default user    ***

# db.drop_all()
# db.create_all()
# Blog.query.delete()

# #  Create blogger users

# vloger = Blog(first_name='Andrew', last_name='Tate')

# vampire = Blog(first_name='Riasn', last_name='star')

# President = Blog(first_name='Barack', last_name='Gentle', image_url='https://wallpapers.com/images/hd/barack-obama-contemplative-portrait-dmlomhkitv6xbvvn-2.png')

# MrSkip = Blog(first_name='Hard', last_name='Head', image_url='https://img.thedailybeast.com/image/upload/c_crop,d_placeholder_euli9k,h_1440,w_2560,x_0,y_0/dpr_1.5/c_limit,w_1044/fl_lossy,q_auto/v1498752576/170629-ryan-trump-tease_ndlqk2')



# db.session.add(vampire)
# db.session.add(vloger)

# db.session.commit()

db.create_all()



#       -------- USER ROUTE------------

@app.route('/')
def user_homepage():
     """Show recent list of posts, most-recent first."""

     posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

     return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route('/users')
def show_user():
    '''Show users on page'''

    users = Blog.query.all()

    bloggers = Blog.query.order_by(Blog.last_name, Blog.first_name).all()

    return render_template('user.html', users=users, bloggers=bloggers)


@app.route('/add/user', methods=['GET'])
def new_user_form():
    '''Show form to add a new blog user to the list'''

    return render_template('new_user.html')


@app.route("/add/user", methods=['POST'])
def new_user():
    '''Handle form for new user submission'''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    new_user = Blog(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users') 


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    '''Show details of a user'''

    user = Blog.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = Blog.query.get(user_id)
    print(user)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = Blog.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = Blog.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



#   _______ ****  POST ROUTE ***______


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    ''' Show a form to new post for a bloger'''

    user = Blog.query.get_or_404(user_id)

    tags = Tag.query.all()
    
    return render_template('new_posts.html', user=user, tags= tags)



@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def  new_post(user_id):
    '''Handles form submission for new post'''

    user = Blog.query.get_or_404(user_id)

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    title = request.form['title']
    content = request.form['content'] 

    new_post = Post(title=title, content=content,blogger=user,tags=tags)
    print(f' new post {new_post}')

    db.session.add(new_post)
    db.session.commit()

    flash(f'your new post {new_post.title} is posted')
    return redirect(f'/users/{user_id}')



@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post,tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.blogger_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.blogger_id}")



# ****************************************************
#       TAG ROUTE

@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5510, debug=True)