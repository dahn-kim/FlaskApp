from flask import render_template, abort, flash, redirect, url_for, request
from app.posts import posts
from flask_login import login_required, current_user
from app.posts.forms import PostForm
from .models import Post
from app import db

@posts.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


@posts.route('/post/add-new', methods =['POST', 'GET'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title= form.title.data,
                    subtitle = form.subtitle.data,
                    content = form.content.data,
                    author = current_user)

        db.session.add(post)
        db.session.commit()
        flash("The Post has been submitted", 'success')
        return redirect(url_for('posts.home'))
    return render_template('add_post.html', form=form, form_title="Add a new post")

@posts.route('/post/<int:post_id>')
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@posts.route('/post/<post_id>/update')
@login_required
def edit_post(post_id):
    posts = post.query.get_or_404(post_id)
    #Check if the current user is the author of the post
    if post.author != current_user:
        abort(403) #http response for forbidden route

    form = PostForm()
    if request.method == "GET":
        form.title.data == post.title
        form.subtitle.data == post.subtitle
        form.content.data == post.text

    elif form.validation_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.text.data

        db.session.commit()
        flash("this post has been updated!", 'success')
        return redirect(url_for('post.single_post', post_id=post.id))

    return render_template('add_post.html', form=form, form_title="Edit Post")

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted.", 'success')
    return redirect(url_for('post.home'))
