"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from books_app.models import Book, Author, Genre, User, favorite_books_table
from books_app.forms import BookForm, AuthorForm, GenreForm, UserForm

# Import app and db from events_app package so that we can run app
from books_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_books = Book.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_books=all_books, all_users=all_users)

@main.route('/create_book', methods=['GET', 'POST'])
def create_book():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_book = Book(
            title = form.title.data,
            publish_date = form.publish_date.data,
            author = form.author.data,
            audience = form.audience.data,
            genres = form.genres.data
        )
        db.session.add(new_book)
        db.session.commit()

        flash('New book was created successfully.')
        return redirect(url_for('main.book_detail', book_id=new_book.id))
    return render_template('create_book.html', form=form)

@main.route('/create_author', methods=['GET', 'POST'])
def create_author():
    form = AuthorForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_author = Author(
            name = form.name.data,
            biography = form.biography.data,
            birth_date = form.birth_date.data,
            country = form.country.data,
        )
        db.session.add(new_author)
        db.session.commit()

        flash('New author was created successfully.')
        return redirect(url_for('main.homepage'))
    return render_template('create_author.html', form=form)

@main.route('/create_genre', methods=['GET', 'POST'])
def create_genre():
    form = GenreForm()

    if form.validate_on_submit():
        new_genre = Genre(
            name = form.name.data,
        )
        db.session.add(new_genre)
        db.session.commit()

        flash('New genre was created successfully.')
        return redirect(url_for('main.homepage'))
    return render_template('create_genre.html', form=form)

@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            favorite_books = form.favorite_books.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash('New book was created successfully.')
        return redirect(url_for('main.profile', username=new_user.username, books=new_user.favorite_books))
    return render_template('create_user.html', form=form)

@main.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.publish_date = form.publish_date.data
        book.author = form.author.data
        book.audience = form.audience.data
        book.genres = form.genres.data

        db.session.add(book)
        db.session.commit()

        flash('Book was successfully edited.')
    return render_template('book_detail.html', book=book, form=form)

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    form = UserForm()
    print(user.favorite_books)
    if form.validate_on_submit():
        user.username = form.username.data

        db.session.commit()
        flash("User successfully updated")
        return redirect(url_for("main.homepage"))
    return render_template("profile.html", username=username, books=user.favorite_books)
