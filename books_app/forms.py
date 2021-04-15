from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length
from books_app.models import Audience, Book, Author, Genre

class BookForm(FlaskForm):
    """Form to create a book."""
    title = StringField('Book Title', validators=[DataRequired(), Length(min=3, max=80)])
    publish_date = DateField('Date Published')
    author = QuerySelectField('Author', query_factory=lambda: Author.query, allow_blank=False)
    audience = SelectField('Audience', choices=Audience.choices())
    genres = QuerySelectMultipleField('Genres', query_factory=lambda: Genre.query)
    submit = SubmitField('Submit')


class AuthorForm(FlaskForm):
    """Form to create an author."""
    name = StringField('Author Name', validators=[DataRequired(), Length(min=1, max=80)])
    biography = TextAreaField('Author Biography', validators=[DataRequired(), Length(min=30, max=400)])
    birth_date = DateField('Birth Date')
    country = StringField('Country')
    submit = SubmitField('Submit')


class GenreForm(FlaskForm):
    """Form to create a genre."""
    name = StringField('Genre Name', validators=[DataRequired(), Length(min=1, max=80)])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    """Form to create a user."""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    favorite_books = QuerySelectMultipleField('Favorite Books', query_factory=lambda: Book.query)
    submit = SubmitField("Submit")
