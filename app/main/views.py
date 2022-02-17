from flask import render_template,redirect,url_for,abort,request,flash
from app.main import main
from .. import db
from app.models import User,Blog,Comment,Subscriber
from app.requests import get_quotes
import secrets
import os
from PIL import Image
from flask_login import login_required,current_user
from .forms import UpdateProfile,CreateBlog
from ..email import mail_message

@main.route('/')
def index():
    quotes = get_quotes()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.order_by(Blog.posted.desc()).paginate(page = page, per_page = 3)
    return render_template('index.html', quote = quotes,blogs=blogs)
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join('app/static/images', picture_filename)
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename

@main.route('/profile',methods = ['POST','GET'])
# @login_required
def profile():
    form = UpdateProfile()
    profile_pic_path = ''
    print('CUURREE', current_user)
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.profile_pic_path = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.bio = form.bio.data
            db.session.commit()
            flash('Succesfully updated your profile')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.bio.data = current_user.bio
            profile_pic_path = url_for('static',filename ='images/'+ current_user.profile_pic_path) 
    return render_template('profile.html', profile_pic_path = profile_pic_path, form = form)    

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('updateprofile.html',form =form)

@main.route('/new_blogpost', methods=['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = CreateBlog()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,content=content,user_id=user_id)
        blog.save()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
    flash('You Posted a new Blog')
    return render_template('newblog.html', form = form)

@main.route('/blog/<blog_id>', methods = ['GET'])
@login_required
def blog(blog_id):
    blog = Blog.query.get(blog_id)
    return render_template('blog.html', blog = blog)

@main.route('/blog/update/<blog_id>', methods = ['GET','POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = CreateBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.blog',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('newblog.html', form = form)

@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
    blog = Blog.query.get(blog_id)
    if request.method == 'POST':
        comment =request.form.get('newcomment')
        new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
        new_comment.save()
    return redirect(url_for('main.blog',blog_id = blog.id))    

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to D-Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.filter_by(user=user).order_by(Blog.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('userposts.html',blogs=blogs,user = user)

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("Blog deleted succesfully!")
    return redirect(url_for('main.index'))

